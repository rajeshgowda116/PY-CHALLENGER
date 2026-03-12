from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from .views import healthcheck_view


def root_redirect(request):
    return redirect("dashboard" if request.user.is_authenticated else "login")


urlpatterns = [
    path("", root_redirect, name="home"),
    path("health/", healthcheck_view, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.problems.urls")),
    path("api/", include("apps.submissions.urls")),
]
