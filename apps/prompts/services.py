from django.db import transaction

from apps.analytics.services import calculate_prompt_score

from .models import Prompt, Tag

def sync_prompt_tags(*, prompt: Prompt, tags_input: str) -> None:
    tag_names = [t.strip().lower() for t in tags_input.split(",") if t.strip()]
    tags = []
    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(
            name=name,
            defaults={"slug": name.replace(" ", "-")},
        )
        tags.append(tag)
    prompt.tags.set(tags)


@transaction.atomic
def create_prompt(*, user, cleaned_data) -> Prompt:
    prompt = Prompt.objects.create(
        user=user,
        source=cleaned_data["source"],
        title=cleaned_data.get("title", ""),
        prompt_text=cleaned_data["prompt_text"],
        response_text=cleaned_data.get("response_text", ""),
        category=cleaned_data["category"],
        rating=cleaned_data["rating"],
        reuse_count=cleaned_data["reuse_count"],
        outcome_metric=cleaned_data.get("outcome_metric", ""),
        outcome_value=cleaned_data["outcome_value"],
        notes=cleaned_data.get("notes", ""),
    )

    prompt.score = calculate_prompt_score(
        rating=prompt.rating,
        reuse_count=prompt.reuse_count,
        outcome_value=prompt.outcome_value,
    )
    prompt.save(update_fields=["score"])
    return prompt


@transaction.atomic
def update_prompt(*, prompt: Prompt, cleaned_data) -> Prompt:
    prompt.source = cleaned_data["source"]
    prompt.title = cleaned_data.get("title", "")
    prompt.prompt_text = cleaned_data["prompt_text"]
    prompt.response_text = cleaned_data.get("response_text", "")
    prompt.category = cleaned_data["category"]
    prompt.rating = cleaned_data["rating"]
    prompt.reuse_count = cleaned_data["reuse_count"]
    prompt.outcome_metric = cleaned_data.get("outcome_metric", "")
    prompt.outcome_value = cleaned_data["outcome_value"]
    prompt.notes = cleaned_data.get("notes", "")

    prompt.score = calculate_prompt_score(
        rating=prompt.rating,
        reuse_count=prompt.reuse_count,
        outcome_value=prompt.outcome_value,
    )
    prompt.save()
    return prompt


@transaction.atomic
def delete_prompt(*, prompt: Prompt) -> None:
    prompt.delete()
