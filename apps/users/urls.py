from django.urls import path

from .forms import StyledAuthenticationForm
from .views import DashboardView, LeaderboardView, RegisterView, SecureLoginView, SecureLogoutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        SecureLoginView.as_view(authentication_form=StyledAuthenticationForm),
        name="login",
    ),
    path("logout/", SecureLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
