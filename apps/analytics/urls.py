from django.urls import path

from .views import DashboardView, LeaderboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]