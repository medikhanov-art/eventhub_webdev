from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from .forms import EventForm
from .models import Event


class HomeView(TemplateView):
    template_name = "events/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(
            is_deleted=False, is_published=True
        ).order_by("starts_at")[:6]
        return context


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    queryset = Event.objects.filter(
        is_deleted=False, is_published=True
    ).order_by("starts_at")


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.filter(is_deleted=False, is_published=True)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    extra_context = {"page_title": "Создать событие"}
    success_url = reverse_lazy("events:event_list")
    login_url = "login"


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    extra_context = {"page_title": "Редактировать событие"}
    success_url = reverse_lazy("events:event_list")
    login_url = "login"

    def get_queryset(self):
        return Event.objects.filter(is_deleted=False)


class EventDeleteView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk, is_deleted=False)
        event.is_deleted = True
        event.save(update_fields=["is_deleted", "updated_at"])
        return redirect("events:event_list")
