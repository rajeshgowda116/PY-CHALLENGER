from django.urls import path

from .views import ProblemWorkspaceView, TopicProblemListView


urlpatterns = [
    path("topics/<slug:slug>/", TopicProblemListView.as_view(), name="topic-problems"),
    path("problems/<slug:slug>/", ProblemWorkspaceView.as_view(), name="problem-workspace"),
]
