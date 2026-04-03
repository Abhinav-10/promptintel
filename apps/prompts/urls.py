from django.urls import path

from .views import (
    PromptCreateView,
    PromptDeleteView,
    PromptDetailView,
    PromptExploreView,
    PromptListView,
    PromptUpdateView,
)

app_name = "prompts"

urlpatterns = [
    path("", PromptListView.as_view(), name="list"),
    path("explore/", PromptExploreView.as_view(), name="explore"),
    path("new/", PromptCreateView.as_view(), name="create"),
    path("<uuid:pk>/", PromptDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", PromptUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", PromptDeleteView.as_view(), name="delete"),
]