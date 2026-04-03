from django.db.models import Prefetch, QuerySet

from .models import Prompt, Tag


def get_user_prompts(*, user) -> QuerySet[Prompt]:
    return (
        Prompt.objects.filter(user=user)
        .prefetch_related(Prefetch("tags", queryset=Tag.objects.order_by("name")))
    )


def get_prompt_by_id(*, user, prompt_id):
    return get_user_prompts(user=user).filter(id=prompt_id).first()


def get_sorted_prompts(*, user, sort_by: str = "newest") -> QuerySet[Prompt]:
    qs = get_user_prompts(user=user)

    if sort_by == "best_score":
        return qs.order_by("-score", "-created_at")
    if sort_by == "highest_rated":
        return qs.order_by("-rating", "-created_at")
    if sort_by == "most_reused":
        return qs.order_by("-reuse_count", "-created_at")
    if sort_by == "highest_outcome":
        return qs.order_by("-outcome_value", "-created_at")

    return qs.order_by("-created_at")


def get_public_prompts(*, sort_by: str = "newest") -> QuerySet[Prompt]:
    """Get all prompts marked as public for the Explore page."""
    qs = (
        Prompt.objects.filter(is_public=True)
        .select_related("user")
        .prefetch_related(Prefetch("tags", queryset=Tag.objects.order_by("name")))
    )

    if sort_by == "best_score":
        return qs.order_by("-score", "-created_at")
    if sort_by == "highest_rated":
        return qs.order_by("-rating", "-created_at")
    if sort_by == "most_reused":
        return qs.order_by("-reuse_count", "-created_at")
    if sort_by == "highest_outcome":
        return qs.order_by("-outcome_value", "-created_at")

    return qs.order_by("-created_at")