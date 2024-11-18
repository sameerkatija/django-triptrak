from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Trip, Note

# Create your views here.
class HomeView(TemplateView):
    template_name = "trips/index.html"

@login_required
def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        'trips' : trips
    }
    return render(request, 'trips/trips_list.html', context)



class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # template_name

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)




class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object'] 
        notes = trip.notes.all()
        context['notes'] = notes
        return context


    



class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note





class NoteListView(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user)
        return queryset
    



class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = "__all__"
    success_url = reverse_lazy("note-list")

    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form




class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = "__all__"
    success_url = reverse_lazy("note-list")

    def get_form(self):
        form = super(NoteUpdateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form





class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("note-list")



class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = reverse_lazy("trip-list")



class TripUpdateView(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['city', 'country', 'start_date', 'end_date']
    success_url = reverse_lazy("trip-list")