from django.urls import path

from .views import ProblemWorkspaceView, TopicProblemListView, add_problem_view


urlpatterns = [
    path("admin-panel/add-problem/", add_problem_view, name="add-problem"),
    path("topics/<slug:slug>/", TopicProblemListView.as_view(), name="topic-problems"),
    path("problems/<slug:slug>/", ProblemWorkspaceView.as_view(), name="problem-workspace"),
]
