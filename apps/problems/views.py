from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.generic import DetailView

from .forms import ProblemAdminForm, TestCaseFormSet
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
        next_problem = (
            Problem.objects.filter(
                topic=self.object.topic,
                is_active=True,
                order__gt=self.object.order,
            )
            .order_by("order", "id")
            .first()
        )
        if next_problem is None:
            next_problem = (
                Problem.objects.filter(
                    topic=self.object.topic,
                    is_active=True,
                    order=self.object.order,
                    id__gt=self.object.id,
                )
                .order_by("order", "id")
                .first()
            )
        context.update(
            {
                "progress": progress,
                "sample_test": self.object.test_cases.filter(is_sample=True).first(),
                "all_topics": Topic.objects.all(),
                "next_problem": next_problem,
            }
        )
        return context


def _generate_unique_problem_slug(title: str) -> str:
    base_slug = slugify(title) or "problem"
    slug = base_slug
    counter = 2
    while Problem.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def _generate_unique_problem_slug_from_value(slug_value: str) -> str:
    base_slug = slugify(slug_value) or "problem"
    slug = base_slug
    counter = 2
    while Problem.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@staff_member_required(login_url="login")
def add_problem_view(request):
    problem = Problem()
    if request.method == "POST":
        form = ProblemAdminForm(request.POST, instance=problem)
        formset = TestCaseFormSet(request.POST, instance=problem, prefix="testcases")

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                problem = form.save(commit=False)
                problem.slug = _generate_unique_problem_slug_from_value(problem.slug or problem.title)
                problem.save()

                test_cases = formset.save(commit=False)
                for deleted_form in formset.deleted_forms:
                    if deleted_form.instance.pk:
                        deleted_form.instance.delete()

                for test_case in test_cases:
                    test_case.problem = problem
                    test_case.save()

            messages.success(request, f'Problem "{problem.title}" was added successfully.')
            return redirect("add-problem")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ProblemAdminForm(instance=problem)
        formset = TestCaseFormSet(instance=problem, prefix="testcases")

    return render(
        request,
        "admin_panel/add_problem.html",
        {
            "form": form,
            "formset": formset,
        },
    )
