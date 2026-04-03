from django.db.models import Avg, Count

from apps.prompts.models import Prompt


def get_dashboard_summary(*, user) -> dict:
    qs = Prompt.objects.filter(user=user)

    total_prompts = qs.count()
    averages = qs.aggregate(
        average_rating=Avg("rating"),
        average_score=Avg("score"),
    )
    top_category_row = (
        qs.values("category")
        .annotate(total=Count("id"))
        .order_by("-total")
        .first()
    )
    top_prompt = qs.order_by("-score", "-created_at").first()

    return {
        "total_prompts": total_prompts,
        "average_rating": round(averages["average_rating"] or 0, 2),
        "average_score": round(float(averages["average_score"] or 0), 2),
        "top_category": top_category_row["category"] if top_category_row else None,
        "top_prompt": top_prompt,
    }


def get_top_prompts(*, user, limit: int = 10):
    return (
        Prompt.objects.filter(user=user)
        .prefetch_related("tags")
        .order_by("-score", "-created_at")[:limit]
    )
