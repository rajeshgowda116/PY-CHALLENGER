from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "problem", "mode", "result", "passed_test_cases", "created_at")
    list_filter = ("mode", "result")
