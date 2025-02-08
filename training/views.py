from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from student.models import Student
from . import forms

"""View de treinos"""
class TrainingListView(ListView):
    model = models.TrainingClass
    template_name = 'training_list.html'
    context_object_name = 'trainings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_seg'] = models.TrainingClass.objects.filter(day='seg')
        context['training_ter'] = models.TrainingClass.objects.filter(day='ter')
        context['training_qua'] = models.TrainingClass.objects.filter(day='qua')
        context['training_qui'] = models.TrainingClass.objects.filter(day='qui')
        context['training_sex'] = models.TrainingClass.objects.filter(day='sex')
        context['training_sab'] = models.TrainingClass.objects.filter(day='sab')
        context['training_dom'] = models.TrainingClass.objects.filter(day='dom')

        return context


class TrainingCreateView(CreateView):
    model = models.TrainingClass
    template_name = 'training_create.html'
    form_class = forms.TrainingModelForm
    success_url = reverse_lazy('training_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtra os estudantes cujo status não seja "Parou"
        context['students'] = Student.objects.exclude(status="Parou")

        return context

class TrainingDetailsView(DetailView):
    model = models.TrainingClass
    template_name = 'training_details.html'


class TrainingUpdateView(UpdateView):
    model = models.TrainingClass
    template_name = 'training_update.html'
    form_class = forms.TrainingModelForm
    success_url = reverse_lazy('training_list')


class TrainingDeleteView(DeleteView):
    model = models.TrainingClass
    template_name = 'training_delete.html'
    success_url = reverse_lazy('training_list')


"""Views de local de treino"""
class LocationTrainingListView(ListView):
    model = models.LocationTraining
    template_name = 'location_training_list.html'
    context_object_name = 'locations'
    paginate_by = 10


class LocationTrainingCreateView(CreateView):
    model = models.LocationTraining
    template_name = 'location_training_create.html'
    form_class = forms.LocationModelForm
    success_url = reverse_lazy('location_training_list')


class LocationTrainingUpdateView(UpdateView):
    model = models.LocationTraining
    template_name = 'location_training_update.html'
    form_class = forms.LocationModelForm
    success_url = reverse_lazy('location_training_list')


class LocationTrainingDetailsView(DetailView):
    model = models.LocationTraining
    template_name = 'location_training_details.html'


class LocationTrainingDeleteView(DeleteView):
    model = models.LocationTraining
    template_name = 'location_training_delete.html'
    success_url = reverse_lazy('location_training_list')
