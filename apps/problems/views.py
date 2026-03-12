from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView

from .models import Problem, ProblemProgress, Topic


class TopicProblemListView(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = "problems/topic_list.html"
    context_object_name = "topic"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        difficulty = self.request.GET.get("difficulty", "")
        search = self.request.GET.get("q", "")
        problems = self.object.problems.filter(is_active=True)
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        if search:
            problems = problems.filter(Q(title__icontains=search) | Q(description__icontains=search))

        progress_map = {
            progress.problem_id: progress
            for progress in ProblemProgress.objects.filter(user=user, problem__in=problems)
        }
        rows = []
        for problem in problems:
            progress = progress_map.get(problem.id)
            rows.append(
                {
                    "problem": problem,
                    "status": "Solved" if progress and progress.is_solved else "Solve",
                    "attempts": progress.attempts if progress else 0,
                }
            )

        context.update(
            {
                "problem_rows": rows,
                "selected_difficulty": difficulty,
                "search_query": search,
            }
        )
        return context


class ProblemWorkspaceView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = "problems/problem_workspace.html"
    context_object_name = "problem"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress, _ = ProblemProgress.objects.get_or_create(user=self.request.user, problem=self.object)
        context.update(
            {
                "progress": progress,
                "sample_test": self.object.test_cases.filter(is_sample=True).first(),
                "all_topics": Topic.objects.all(),
            }
        )
        return context
