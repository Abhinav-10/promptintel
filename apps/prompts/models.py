from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel, UUIDModel


class PromptCategory(models.TextChoices):
    CONTENT = "content", "Content"
    CODING = "coding", "Coding"
    BUSINESS = "business", "Business"
    LEARNING = "learning", "Learning"
    RESEARCH = "research", "Research"
    OTHER = "other", "Other"


class PromptSource(models.TextChoices):
    MANUAL = "manual", "Manual"
    CHATGPT = "chatgpt", "ChatGPT"
    CLAUDE = "claude", "Claude"
    GEMINI = "gemini", "Gemini"
    OTHER = "other", "Other"


class OutcomeMetric(models.TextChoices):
    VIEWS = "views", "Views"
    CLICKS = "clicks", "Clicks"
    LEADS = "leads", "Leads"
    REVENUE = "revenue", "Revenue"
    TIME_SAVED = "time_saved", "Time Saved"
    OTHER = "other", "Other"


class Tag(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Prompt(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="prompts",
    )
    source = models.CharField(
        max_length=20,
        choices=PromptSource.choices,
        default=PromptSource.MANUAL,
    )
    title = models.CharField(max_length=120, blank=True)
    prompt_text = models.TextField()
    response_text = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=PromptCategory.choices,
        default=PromptCategory.OTHER,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="prompts")
    rating = models.PositiveSmallIntegerField(default=0)
    reuse_count = models.PositiveIntegerField(default=0)
    outcome_metric = models.CharField(
        max_length=20,
        choices=OutcomeMetric.choices,
        blank=True,
    )
    outcome_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    notes = models.TextField(blank=True)
    score = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Allow this prompt to be visible on the public Explore page",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "category"]),
            models.Index(fields=["user", "-score"]),
            models.Index(fields=["user", "-rating"]),
        ]

    def __str__(self):
        return self.title or self.prompt_text[:60]