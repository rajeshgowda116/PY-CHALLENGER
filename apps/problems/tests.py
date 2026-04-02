from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Problem, Topic


class AddProblemViewTests(TestCase):
    def setUp(self):
        suffix = self._testMethodName.replace("_", "-")
        self.topic = Topic.objects.create(
            title=f"Arrays {suffix}",
            slug=f"arrays-{suffix}",
            description="Array practice",
            order=1,
        )
        self.staff_user = User.objects.create_user(
            username=f"adminuser-{suffix}",
            password="strong-pass-123",
            is_staff=True,
        )
        self.normal_user = User.objects.create_user(
            username=f"regularuser-{suffix}",
            password="strong-pass-123",
        )
        self.url = reverse("add-problem")

    def _valid_payload(self):
        return {
            "topic": str(self.topic.pk),
            "title": "Two Sum Variant",
            "slug": "two-sum-custom",
            "difficulty": "easy",
            "description": "Return the matching pair indexes.",
            "instructions": "Use zero-based indexing.",
            "starter_code": "def solve():\n    pass",
            "solution": "def solve():\n    print('ok')",
            "example_input": "4\n1 2 3 4\n5",
            "example_output": "1 4",
            "order": "7",
            "is_active": "on",
            "points": "25",
            "testcases-TOTAL_FORMS": "2",
            "testcases-INITIAL_FORMS": "0",
            "testcases-MIN_NUM_FORMS": "0",
            "testcases-MAX_NUM_FORMS": "1000",
            "testcases-0-input_data": "4\n1 2 3 4\n5",
            "testcases-0-expected_output": "1 4",
            "testcases-0-is_sample": "on",
            "testcases-0-order": "3",
            "testcases-1-input_data": "3\n2 7 11\n9",
            "testcases-1-expected_output": "0 1",
            "testcases-1-order": "5",
        }

    def test_non_staff_user_cannot_access_page(self):
        self.client.login(username=self.normal_user.username, password="strong-pass-123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_staff_user_can_create_problem_with_test_cases(self):
        self.client.login(username=self.staff_user.username, password="strong-pass-123")

        response = self.client.post(self.url, data=self._valid_payload(), follow=True)

        self.assertRedirects(response, self.url)
        problem = Problem.objects.get(title="Two Sum Variant")
        self.assertEqual(problem.slug, "two-sum-custom")
        self.assertEqual(problem.solution, "def solve():\n    print('ok')")
        self.assertEqual(problem.instructions, "Use zero-based indexing.")
        self.assertEqual(problem.example_input, "4\n1 2 3 4\n5")
        self.assertEqual(problem.example_output, "1 4")
        self.assertEqual(problem.order, 7)
        self.assertEqual(problem.points, 25)
        self.assertTrue(problem.is_active)
        self.assertFalse(problem.is_daily_challenge)
        self.assertEqual(problem.test_cases.count(), 2)
        first_test_case = problem.test_cases.order_by("order").first()
        self.assertTrue(first_test_case.is_sample)
        self.assertEqual(first_test_case.order, 3)
        messages = list(response.context["messages"])
        self.assertTrue(any("added successfully" in str(message) for message in messages))

    def test_requires_at_least_one_complete_test_case(self):
        self.client.login(username=self.staff_user.username, password="strong-pass-123")
        payload = self._valid_payload()
        payload["testcases-0-input_data"] = ""
        payload["testcases-0-expected_output"] = ""
        payload["testcases-1-input_data"] = ""
        payload["testcases-1-expected_output"] = ""

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add at least one test case with an expected output before saving the problem.")
        self.assertFalse(Problem.objects.filter(title="Two Sum Variant").exists())

    def test_allows_blank_input_data_when_expected_output_exists(self):
        self.client.login(username=self.staff_user.username, password="strong-pass-123")
        payload = self._valid_payload()
        payload["testcases-0-input_data"] = ""

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertRedirects(response, self.url)
        self.assertTrue(Problem.objects.filter(title="Two Sum Variant").exists())
        problem = Problem.objects.get(title="Two Sum Variant")
        self.assertEqual(problem.test_cases.order_by("order").first().input_data, "")
