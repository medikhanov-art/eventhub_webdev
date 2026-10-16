from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.views import View


class HomeView(TemplateView):
    template_name = "events/home.html"


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = "/events/"

def event_detail(request, slug):
    """Детальная страница выбранного события."""
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, 'events/event_detail.html', {'event': event})

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = "/events/"

class EventDeleteView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.is_deleted = True
        event.save()
        return redirect('events:event_list')

def home(request):
    events = Event.objects.all().order_by('-starts_at')[:6] # берем первые 6 ивентов
    return render(request, 'events/home.html', {'events': events})
# Comment