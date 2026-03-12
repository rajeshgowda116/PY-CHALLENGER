from django.contrib import admin

from .models import Problem, ProblemProgress, TestCase, Topic


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "accent_color")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "difficulty", "points", "is_daily_challenge", "is_active")
    list_filter = ("difficulty", "topic", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TestCaseInline]


@admin.register(ProblemProgress)
class ProblemProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "problem", "is_solved", "attempts", "updated_at")
    list_filter = ("is_solved", "problem__topic")
