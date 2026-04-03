from django import forms

from .models import OutcomeMetric, Prompt, Tag


class PromptForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags",
    )

    class Meta:
        model = Prompt
        fields = [
            "source",
            "title",
            "prompt_text",
            "response_text",
            "category",
            "rating",
            "reuse_count",
            "outcome_metric",
            "outcome_value",
            "notes",
            "is_public",
        ]
        widgets = {
            "prompt_text": forms.Textarea(attrs={"rows": 6}),
            "response_text": forms.Textarea(attrs={"rows": 6}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["prompt_text"].label = "Prompt"
        self.fields["response_text"].label = "Prompt Experience"
        self.fields["response_text"].required = False
        self.fields["response_text"].help_text = (
            "Optional: for long AI outputs, capture a concise summary, key snippet, "
            "or what worked vs. failed."
        )
        self.fields["response_text"].widget.attrs.update(
            {
                "rows": 10,
                "placeholder": (
                    "You don't need to paste the full model response. "
                    "Add a useful summary of the output quality, strengths, and gaps."
                ),
            }
        )

        self.fields["outcome_metric"].label = "Impact Metric (Optional)"
        self.fields["outcome_metric"].required = False
        self.fields["outcome_metric"].choices = [
            ("", "No metric yet"),
            (OutcomeMetric.TIME_SAVED, "Time Saved (minutes/hours)"),
            (OutcomeMetric.TASKS_COMPLETED, "Tasks Completed"),
            (OutcomeMetric.QUALITY_SCORE, "Quality Score (1-10)"),
            (OutcomeMetric.ACCURACY, "Accuracy (%)"),
            (OutcomeMetric.USER_SATISFACTION, "User Satisfaction (CSAT/NPS)"),
            (OutcomeMetric.COST_SAVED, "Cost Saved"),
            (OutcomeMetric.REVENUE, "Revenue Impact"),
            (OutcomeMetric.VIEWS, "Views / Reach"),
            (OutcomeMetric.CLICKS, "Action Clicks"),
            (OutcomeMetric.LEADS, "Lead Generation"),
            (OutcomeMetric.OTHER, "Custom Metric"),
        ]

        self.fields["outcome_value"].label = "Impact Value (Optional)"
        self.fields["outcome_value"].required = False
        self.fields["outcome_value"].widget.attrs.update(
            {"placeholder": "Example: 120 (minutes), 8 (tasks), 4.6 (quality score)"}
        )
        self.fields["notes"].widget.attrs.update(
            {
                "placeholder": (
                    "Capture learnings: when this prompt works best, "
                    "what to tweak next time, and edge cases."
                )
            }
        )

        if self.instance.pk:
            self.fields["tags_input"].initial = ", ".join(
                self.instance.tags.values_list("name", flat=True)
            )

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating

    def clean(self):
        cleaned_data = super().clean()
        outcome_metric = cleaned_data.get("outcome_metric")
        outcome_value = cleaned_data.get("outcome_value")

        if outcome_metric and outcome_value is None:
            self.add_error(
                "outcome_value",
                "Please add an impact value when an impact metric is selected.",
            )

        if not outcome_metric:
            cleaned_data["outcome_value"] = 0

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags_raw = self.cleaned_data.get("tags_input", "")
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(
                    name=name,
                    defaults={"slug": name.replace(" ", "-")},
                )
                tags.append(tag)
            instance.tags.set(tags)
        return instance
