from functools import wraps

from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self' https://cdn.jsdelivr.net; "
            "worker-src 'self' blob: https://cdn.jsdelivr.net; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers.setdefault("Content-Security-Policy", csp)
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        return response


def _client_identifier(request):
    if getattr(request, "user", None) and request.user.is_authenticated:
        return f"user:{request.user.pk}"
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def ratelimit(key_prefix: str, limit: int, window: int, json_response: bool = False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            identity = f"{key_prefix}:{_client_identifier(request)}"
            current = cache.get(identity, 0)
            if current >= limit:
                if json_response:
                    return JsonResponse({"error": "Rate limit exceeded. Please try again later."}, status=429)
                return HttpResponseForbidden("Too many requests. Please try again later.")
            cache.set(identity, current + 1, timeout=window)
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
