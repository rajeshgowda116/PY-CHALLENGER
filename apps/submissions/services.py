import subprocess
import tempfile
from pathlib import Path
from collections.abc import Sized

from django.conf import settings
from django.utils import timezone

from apps.problems.models import Problem, ProblemProgress

from .models import Submission

BLOCKED_TOKENS = ["import os", "import sys", "subprocess", "open(", "exec(", "eval(", "__import__", "from os", "from sys", "pathlib"]


class CodeExecutionDisabledError(Exception):
    pass


def normalize_output(value: str) -> str:
    lines = value.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip()


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
    if mode == "run":
        sample_cases = problem.test_cases.filter(is_sample=True)
        if sample_cases.exists():
            cases = sample_cases
        elif problem.example_input or problem.example_output:
            cases = [
                {
                    "input_data": problem.example_input,
                    "expected_output": problem.example_output,
                }
            ]
        else:
            cases = problem.test_cases.all()[:1]
    else:
        cases = problem.test_cases.all()
    total_cases = cases.count() if hasattr(cases, "model") else (len(cases) if isinstance(cases, Sized) else 0)
    passed = 0
    final_output = ""
    final_error = ""
    final_result = "accepted"

    if total_cases == 0:
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            mode=mode,
            result="runtime_error",
            output="",
            error_message="No test cases are configured for this problem.",
            passed_test_cases=0,
            total_test_cases=0,
        )
        return submission

    for case in cases:
        input_data = case.input_data if hasattr(case, "input_data") else case["input_data"]
        expected_output = case.expected_output if hasattr(case, "expected_output") else case["expected_output"]
        try:
            execution = execute_python_code(code, input_data)
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
        normalized_output = normalize_output(execution["output"])
        normalized_expected = normalize_output(expected_output)
        if normalized_output != normalized_expected:
            final_result = "wrong_answer"
            final_error = f"Expected:\n{normalized_expected or '[empty]'}\n\nReceived:\n{normalized_output or '[empty]'}"
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
