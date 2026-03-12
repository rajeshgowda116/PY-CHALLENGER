import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from apps.problems.models import Problem, ProblemProgress

from .models import Submission

BLOCKED_TOKENS = ["import os", "import sys", "subprocess", "open(", "exec(", "eval(", "__import__", "from os", "from sys", "pathlib"]


class CodeExecutionDisabledError(Exception):
    pass


def validate_code_safety(code: str):
    lowered = code.lower()
    for token in BLOCKED_TOKENS:
        if token in lowered:
            return False, f"Blocked token detected: {token}"
    return True, ""


def execute_python_code(code: str, stdin_data: str):
    if not settings.ENABLE_LOCAL_CODE_EXECUTION:
        raise CodeExecutionDisabledError(
            "Code execution is disabled in this environment. Configure an isolated execution worker for production."
        )

    if len(code) > settings.MAX_SOURCE_SIZE:
        return {"result": "runtime_error", "output": "", "error": "Submitted code exceeds the maximum allowed size."}

    safe, reason = validate_code_safety(code)
    if not safe:
        return {"result": "runtime_error", "output": "", "error": reason}

    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "solution.py"
        script_path.write_text(code, encoding="utf-8")
        try:
            completed = subprocess.run(
                ["python", str(script_path)],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=settings.CODE_EXECUTION_TIME_LIMIT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "result": "timeout",
                "output": "",
                "error": f"Execution timed out after {settings.CODE_EXECUTION_TIME_LIMIT_SECONDS} seconds.",
            }

    if completed.returncode != 0:
        return {
            "result": "runtime_error",
            "output": completed.stdout.strip(),
            "error": completed.stderr.strip() or "Unknown runtime error.",
        }
    return {"result": "accepted", "output": completed.stdout.strip(), "error": ""}


def run_problem_code(user, problem: Problem, code: str, mode: str):
    cases = problem.test_cases.filter(is_sample=True) if mode == "run" else problem.test_cases.all()
    total_cases = cases.count()
    passed = 0
    final_output = ""
    final_error = ""
    final_result = "accepted"

    for case in cases:
        try:
            execution = execute_python_code(code, case.input_data)
        except CodeExecutionDisabledError as exc:
            submission = Submission.objects.create(
                user=user,
                problem=problem,
                code=code,
                mode=mode,
                result="runtime_error",
                output="",
                error_message=str(exc),
                passed_test_cases=0,
                total_test_cases=total_cases,
            )
            return submission
        final_output = execution["output"]
        final_error = execution["error"]
        if execution["result"] != "accepted":
            final_result = execution["result"]
            break
        if execution["output"].strip() != case.expected_output.strip():
            final_result = "wrong_answer"
            final_error = f"Expected: {case.expected_output.strip()} | Received: {execution['output'].strip() or '[empty]'}"
            break
        passed += 1

    submission = Submission.objects.create(
        user=user,
        problem=problem,
        code=code,
        mode=mode,
        result=final_result,
        output=final_output,
        error_message=final_error,
        passed_test_cases=passed,
        total_test_cases=total_cases,
    )

    progress, _ = ProblemProgress.objects.get_or_create(user=user, problem=problem)
    progress.attempts += 1
    progress.last_submitted_code = code
    progress.last_result = submission.get_result_display()
    if final_result == "accepted" and mode == "submit":
        if not progress.is_solved:
            progress.is_solved = True
            progress.solved_at = timezone.now()
            user.profile.total_points += problem.points
            user.profile.save(update_fields=["total_points"])
        user.profile.register_solve_for_today()
    progress.save()

    return submission
