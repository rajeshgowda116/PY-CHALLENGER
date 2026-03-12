from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from apps.problems.models import Problem, ProblemProgress, Topic
from config.security import ratelimit

from .forms import RegisterForm


@method_decorator(ratelimit("login", limit=10, window=300), name="dispatch")
class SecureLoginView(auth_views.LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class SecureLogoutView(auth_views.LogoutView):
    http_method_names = ["post", "options"]


@method_decorator(ratelimit("register", limit=5, window=300), name="dispatch")
class RegisterView(FormView):
    template_name = "auth/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.first_name = form.cleaned_data["first_name"].strip()
        user.last_name = form.cleaned_data["last_name"].strip()
        user.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully.")
        return redirect("dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        solved_problem_ids = set(
            ProblemProgress.objects.filter(user=user, is_solved=True).values_list("problem_id", flat=True)
        )
        topics = Topic.objects.annotate(total_problems=Count("problems")).order_by("order", "title")
        topic_cards = []
        for topic in topics:
            topic_problem_ids = set(topic.problems.values_list("id", flat=True))
            solved_count = len(solved_problem_ids & topic_problem_ids)
            topic_cards.append(
                {
                    "topic": topic,
                    "total": topic.total_problems,
                    "solved": solved_count,
                    "remaining": max(topic.total_problems - solved_count, 0),
                }
            )

        solved_count = len(solved_problem_ids)
        attempted_count = ProblemProgress.objects.filter(user=user).count()
        context.update(
            {
                "topic_cards": topic_cards,
                "solved_count": solved_count,
                "attempted_count": attempted_count,
                "activity_completion": int((solved_count / max(Problem.objects.count(), 1)) * 100),
                "daily_challenge": Problem.objects.filter(is_daily_challenge=True).select_related("topic").first(),
                "leaderboard": User.objects.filter(profile__isnull=False)
                .select_related("profile")
                .annotate(solved_total=Count("problem_progress", filter=Q(problem_progress__is_solved=True)))
                .order_by("-profile__total_points", "-profile__current_streak", "username")[:10],
                "recent_progress": ProblemProgress.objects.filter(user=user, is_solved=True)
                .select_related("problem", "problem__topic")
                .order_by("-updated_at")[:5],
            }
        )
        return context


class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = "leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = (
            User.objects.filter(profile__isnull=False)
            .select_related("profile")
            .annotate(solved_total=Count("problem_progress", filter=Q(problem_progress__is_solved=True)))
            .order_by("-profile__total_points", "-profile__current_streak", "username")
        )
        return context
