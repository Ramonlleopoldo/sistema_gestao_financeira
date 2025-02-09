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
        trainings = context['trainings']
        location_training = models.LocationTraining.objects.all()
        
        # Dividir os treinos por dia
        context['training_days'] = {
            'seg': trainings.filter(day='seg'),
            'ter': trainings.filter(day='ter'),
            'qua': trainings.filter(day='qua'),
            'qui': trainings.filter(day='qui'),
            'sex': trainings.filter(day='sex'),
            'sab': trainings.filter(day='sab'),
            'dom': trainings.filter(day='dom'),
        }
        # Capturando quantidade de treinos em cada local
        brasil = 0
        criciuma = 0
        for training in context['trainings']:
            if training.location.name == "Arena Brasil":
                brasil += 1 
            elif training.location.name == "Arena Criciuma":
                criciuma += 1
        context['brasil'] = brasil
        context['criciuma'] = criciuma
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            print(f'Filtramos por {name}')
            queryset = queryset.filter(student__name__icontains=name).distinct()
        return queryset


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
