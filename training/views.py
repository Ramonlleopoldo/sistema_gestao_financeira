from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from student.models import Student
from . import forms

"""View de treinos"""
class TrainingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.TrainingClass
    template_name = 'training/training_list.html'
    context_object_name = 'trainings'
    permission_required = 'training.view_trainingclass'

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


class TrainingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.TrainingClass
    template_name = 'training/training_create.html'
    form_class = forms.TrainingModelForm
    success_url = reverse_lazy('training_list')
    permission_required = 'training.add_trainingclass'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtra os estudantes cujo status não seja "Parou"
        context['students'] = Student.objects.exclude(status="Parou")

        return context

class TrainingDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.TrainingClass
    template_name = 'training/training_details.html'
    permission_required = 'training.view_trainingclass'


class TrainingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.TrainingClass
    template_name = 'training/training_update.html'
    form_class = forms.TrainingModelForm
    success_url = reverse_lazy('training_list')
    permission_required = 'training.change_trainingclass'


class TrainingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.TrainingClass
    template_name = 'training/training_delete.html'
    success_url = reverse_lazy('training_list')
    permission_required = 'training.delete_trainingclass'


"""Views de local de treino"""
class LocationTrainingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.LocationTraining
    template_name = 'location_training/location_training_list.html'
    context_object_name = 'locations'
    paginate_by = 10
    permission_required = 'training.view_locationtraining'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Verifica se já existem pelo menos dois locais de treino
        if models.LocationTraining.objects.count() < 2:
            # Se não existirem, cria dois locais padrão
            models.LocationTraining.objects.create(name="Arena Brasil")
            models.LocationTraining.objects.create(name="Arena Criciuma")

        return context


class LocationTrainingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.LocationTraining
    template_name = 'location_training/location_training_create.html'
    form_class = forms.LocationModelForm
    success_url = reverse_lazy('location_training_list')
    permission_required = 'training.add_locationtraining'


class LocationTrainingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.LocationTraining
    template_name = 'location_training/location_training_update.html'
    form_class = forms.LocationModelForm
    success_url = reverse_lazy('location_training_list')
    permission_required = 'training.change_locationtraining'


class LocationTrainingDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.LocationTraining
    template_name = 'location_training/location_training_details.html'
    permission_required = 'training.view_locationtraining'


class LocationTrainingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.LocationTraining
    template_name = 'location_training/location_training_delete.html'
    success_url = reverse_lazy('location_training_list')
    permission_required = 'training.delete_locationtraining'
