from django import forms

from .models import Prompt, Tag


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
        if self.instance.pk:
            self.fields["tags_input"].initial = ", ".join(
                self.instance.tags.values_list("name", flat=True)
            )

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating

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