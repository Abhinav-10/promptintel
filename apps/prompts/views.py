from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import PromptForm
from .selectors import get_prompt_by_id, get_public_prompts, get_sorted_prompts
from .services import create_prompt, delete_prompt, update_prompt, sync_prompt_tags


class PromptListView(LoginRequiredMixin, ListView):
    template_name = "prompts/prompt_list.html"
    context_object_name = "prompts"
    paginate_by = 20

    def get_queryset(self):
        sort_by = self.request.GET.get("sort", "best_score")
        return get_sorted_prompts(user=self.request.user, sort_by=sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort"] = self.request.GET.get("sort", "best_score")
        return context


class PromptDetailView(LoginRequiredMixin, DetailView):
    template_name = "prompts/prompt_detail.html"
    context_object_name = "prompt"

    def get_object(self, queryset=None):
        prompt = get_prompt_by_id(user=self.request.user, prompt_id=self.kwargs["pk"])
        if not prompt:
            raise Http404("Prompt not found")
        return prompt


class PromptCreateView(LoginRequiredMixin, View):
    template_name = "prompts/prompt_form.html"

    def get(self, request):
        form = PromptForm()
        return render(request, self.template_name, {"form": form, "mode": "create"})

    def post(self, request):
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = create_prompt(user=request.user, cleaned_data=form.cleaned_data)
            sync_prompt_tags(
                prompt=prompt,
                tags_input=form.cleaned_data.get("tags_input", ""),
            )
            return redirect("prompts:detail", pk=prompt.pk)

        return render(request, self.template_name, {"form": form, "mode": "create"})


class PromptUpdateView(LoginRequiredMixin, View):
    template_name = "prompts/prompt_form.html"

    def get_object(self, request, pk):
        prompt = get_prompt_by_id(user=request.user, prompt_id=pk)
        if not prompt:
            raise Http404("Prompt not found")
        return prompt

    def get(self, request, pk):
        prompt = self.get_object(request, pk)
        form = PromptForm(instance=prompt)
        return render(
            request,
            self.template_name,
            {"form": form, "prompt": prompt, "mode": "update"},
        )

    def post(self, request, pk):
        prompt = self.get_object(request, pk)
        form = PromptForm(request.POST, instance=prompt)
        if form.is_valid():
            prompt = update_prompt(prompt=prompt, cleaned_data=form.cleaned_data)
            sync_prompt_tags(
                prompt=prompt,
                tags_input=form.cleaned_data.get("tags_input", ""),
            )
            return redirect("prompts:detail", pk=prompt.pk)

        return render(
            request,
            self.template_name,
            {"form": form, "prompt": prompt, "mode": "update"},
        )


class PromptDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        prompt = get_prompt_by_id(user=request.user, prompt_id=pk)
        if not prompt:
            raise Http404("Prompt not found")
        delete_prompt(prompt=prompt)
        return redirect("prompts:list")


class PromptExploreView(ListView):
    """Public page showing all prompts marked as public."""
    template_name = "prompts/prompt_explore.html"
    context_object_name = "prompts"
    paginate_by = 20

    def get_queryset(self):
        sort_by = self.request.GET.get("sort", "newest")
        return get_public_prompts(sort_by=sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort"] = self.request.GET.get("sort", "newest")
        return context