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


@login_required
@require_POST
@ratelimit("run-code", limit=30, window=300, json_response=True)
def run_code_view(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    payload = _parse_payload(request)
    submission = run_problem_code(request.user, problem, payload.get("code", ""), "run")
    progress = ProblemProgress.objects.filter(user=request.user, problem=problem).first()
    return JsonResponse(
        {
            "result": submission.get_result_display(),
            "output": submission.output,
            "error": submission.error_message,
            "passed": submission.passed_test_cases,
            "total": submission.total_test_cases,
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
    return JsonResponse(
        {
            "result": submission.get_result_display(),
            "output": submission.output,
            "error": submission.error_message,
            "passed": submission.passed_test_cases,
            "total": submission.total_test_cases,
            "attempts": progress.attempts if progress else 0,
        }
    )
