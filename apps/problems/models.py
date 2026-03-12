from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    accent_color = models.CharField(max_length=20, default="#1f6feb")

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="problems")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    starter_code = models.TextField(default="def solve():\n    pass\n")
    example_input = models.TextField(blank=True)
    example_output = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_daily_challenge = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = ("topic", "title")

    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.TextField(blank=True)
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.problem.title} test #{self.pk}"


class ProblemProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="problem_progress")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="progress_records")
    is_solved = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    last_submitted_code = models.TextField(blank=True)
    last_result = models.CharField(max_length=40, blank=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "problem")

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
