from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=255, blank=True)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_solved_on = models.DateField(null=True, blank=True)
    total_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def register_solve_for_today(self):
        today = timezone.localdate()
        if self.last_solved_on == today:
            return
        if self.last_solved_on == today - timezone.timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_solved_on = today
        self.save(update_fields=["current_streak", "longest_streak", "last_solved_on"])
