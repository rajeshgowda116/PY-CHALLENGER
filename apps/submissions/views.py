import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.problems.models import Problem, ProblemProgress
from config.security import ratelimit

from .services import run_problem_code


def _parse_payload(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def _serialize_case_results(submission):
    return [
        {
            "index": case["index"],
            "status": case["status"].replace("_", " ").title(),
            "input": case["input"],
            "expected": case["expected"],
            "received": case["received"],
            "error": case["error"],
        }
        for case in getattr(submission, "case_results", [])
    ]


def _build_case_report(cases):
    if not cases:
        return ""

    blocks = []
    for case in cases:
        parts = [f"Case {case['index']}: {case['status']}"]
        if case["input"]:
            parts.append(f"Input:\n{case['input']}")
        if case["expected"]:
            parts.append(f"Expected:\n{case['expected']}")
        if case["received"]:
            parts.append(f"Received:\n{case['received']}")
        if case["error"]:
            parts.append(f"Error:\n{case['error']}")
        blocks.append("\n\n".join(parts))

    return "\n\n--------------------\n\n".join(blocks)


@login_required
@require_POST
@ratelimit("run-code", limit=30, window=300, json_response=True)
def run_code_view(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    payload = _parse_payload(request)
    submission = run_problem_code(request.user, problem, payload.get("code", ""), "run")
    progress = ProblemProgress.objects.filter(user=request.user, problem=problem).first()
    cases = _serialize_case_results(submission)
    return JsonResponse(
        {
            "result": submission.get_result_display(),
            "output": _build_case_report(cases) or submission.output,
            "error": submission.error_message,
            "passed": submission.passed_test_cases,
            "total": submission.total_test_cases,
            "cases": cases,
            "attempts": progress.attempts if progress else 0,
        }
    )


@login_required
@require_POST
@ratelimit("submit-code", limit=20, window=300, json_response=True)
def submit_code_view(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    payload = _parse_payload(request)
    submission = run_problem_code(request.user, problem, payload.get("code", ""), "submit")
    progress = ProblemProgress.objects.filter(user=request.user, problem=problem).first()
    cases = _serialize_case_results(submission)
    return JsonResponse(
        {
            "result": submission.get_result_display(),
            "output": _build_case_report(cases) or submission.output,
            "error": submission.error_message,
            "passed": submission.passed_test_cases,
            "total": submission.total_test_cases,
            "cases": cases,
            "attempts": progress.attempts if progress else 0,
        }
    )
