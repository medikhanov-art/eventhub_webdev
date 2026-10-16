from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    starts_at = forms.DateTimeField(
        label="Дата и время",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Event
        fields = ["title", "slug", "summary", "description", "poster", "starts_at", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Django Meetup"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "django-meetup"}),
            "summary": forms.TextInput(attrs={"class": "form-control", "placeholder": "Коротко о событии"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Что ждёт участников?"}),
            "poster": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
