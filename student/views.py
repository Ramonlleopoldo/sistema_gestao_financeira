from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from . import models
from . import forms


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 10
    permission_required = 'student.view_student'

    def get_context_data(self, **kwargs):
        """Recuperando os choices de level_choices e gender_choices para ser usado em filtros"""
        context = super().get_context_data(**kwargs)
        context['level_choices'] = models.LEVEL_CHOICES
        context['gender_choices'] = models.GENDER_CHOICES

        return context

    def get_queryset(self):
        """Filtros por name, level e gender"""
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        level = self.request.GET.get('level')
        gender = self.request.GET.get('gender')

        if name:
            queryset = models.Student.objects.filter(name__icontains=name)
        if level:
            queryset = queryset.filter(level=level)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Student
    form_class = forms.StudentModelForm
    template_name = 'student_create.html'
    success_url = reverse_lazy('student_list')
    permission_required = 'student.add_student'


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Student
    template_name = 'student_detail.html'
    permission_required = 'student.view_student'


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Student
    form_class = forms.StudentModelForm
    template_name = 'student_update.html'
    success_url = reverse_lazy('student_list')
    permission_required = 'student.change_student'
