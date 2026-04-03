from django.contrib import admin

from .models import Prompt, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "source",
        "category",
        "rating",
        "reuse_count",
        "outcome_metric",
        "outcome_value",
        "score",
        "created_at",
    )
    list_filter = ("source", "category", "outcome_metric", "created_at")
    search_fields = ("title", "prompt_text", "response_text", "notes")
    readonly_fields = ("score", "created_at", "updated_at")
    filter_horizontal = ("tags",)