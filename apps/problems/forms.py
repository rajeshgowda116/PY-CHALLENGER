from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Problem, TestCase


class ProblemAdminForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            "topic",
            "title",
            "slug",
            "difficulty",
            "description",
            "instructions",
            "starter_code",
            "solution",
            "example_input",
            "example_output",
            "order",
            "is_active",
            "is_daily_challenge",
            "points",
        ]
        widgets = {
            "topic": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Enter a clear problem title",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Auto-generated from title if left blank",
                }
            ),
            "difficulty": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Describe the challenge, constraints, and expected behavior.",
                }
            ),
            "instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Optional extra instructions for the solver.",
                }
            ),
            "starter_code": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 10,
                    "placeholder": "def solve():\n    pass",
                }
            ),
            "solution": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 10,
                    "placeholder": "Provide the reference solution used by admins.",
                }
            ),
            "example_input": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": "Optional example input shown to the user",
                }
            ),
            "example_output": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": "Optional example output shown to the user",
                }
            ),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_daily_challenge": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "points": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_slug(self):
        return (self.cleaned_data.get("slug") or "").strip()

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if not description:
            raise forms.ValidationError("Description is required.")
        return description

    def clean_solution(self):
        solution = self.cleaned_data["solution"].strip()
        if not solution:
            raise forms.ValidationError("Solution is required.")
        return solution


class BaseTestCaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_test_case = False
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE"):
                continue

            input_data = (form.cleaned_data.get("input_data") or "").strip()
            expected_output = (form.cleaned_data.get("expected_output") or "").strip()
            if expected_output:
                has_test_case = True

            if input_data and not expected_output:
                form.add_error("expected_output", "Expected output is required when a test case is added.")

        if not has_test_case:
            raise forms.ValidationError("Add at least one test case with an expected output before saving the problem.")


TestCaseFormSet = inlineformset_factory(
    Problem,
    TestCase,
    fields=("input_data", "expected_output", "is_sample", "order"),
    extra=1,
    can_delete=True,
    formset=BaseTestCaseInlineFormSet,
    widgets={
        "input_data": forms.Textarea(
            attrs={
                "class": "form-control font-monospace",
                "rows": 4,
                "placeholder": "Input data for this test case",
            }
        ),
        "expected_output": forms.Textarea(
            attrs={
                "class": "form-control font-monospace",
                "rows": 4,
                "placeholder": "Expected output",
            }
        ),
        "is_sample": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        "order": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
    },
)
