from django.contrib.auth.models import User
from django.db import models

from apps.problems.models import Problem


class Submission(models.Model):
    RESULT_CHOICES = [
        ("accepted", "Accepted"),
        ("wrong_answer", "Wrong Answer"),
        ("runtime_error", "Runtime Error"),
        ("timeout", "Timeout"),
    ]
    MODE_CHOICES = [
        ("run", "Run"),
        ("submit", "Submit"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    passed_test_cases = models.PositiveIntegerField(default=0)
    total_test_cases = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.result}"
