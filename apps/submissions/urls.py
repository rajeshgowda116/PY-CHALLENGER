from django.urls import path

from .views import run_code_view, submit_code_view


urlpatterns = [
    path("problems/<slug:slug>/run/", run_code_view, name="run-code"),
    path("problems/<slug:slug>/submit/", submit_code_view, name="submit-code"),
]
