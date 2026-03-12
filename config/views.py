from django.conf import settings
from django.http import JsonResponse


def healthcheck_view(request):
    return JsonResponse(
        {
            "status": "ok",
            "debug": settings.DEBUG,
            "code_execution_enabled": settings.ENABLE_LOCAL_CODE_EXECUTION,
        }
    )
