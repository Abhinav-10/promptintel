from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.prompts.selectors import get_sorted_prompts

from .selectors import get_dashboard_summary, get_top_prompts


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = get_dashboard_summary(user=self.request.user)
        context["prompts"] = get_sorted_prompts(
            user=self.request.user,
            sort_by="best_score",
        )[:10]
        context["top_prompts"] = get_top_prompts(user=self.request.user, limit=5)
        return context


class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_prompts"] = get_top_prompts(user=self.request.user, limit=20)
        return context
