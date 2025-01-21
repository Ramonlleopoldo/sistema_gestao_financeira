from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms


class StudentListView(ListView):
    model = models.Student
    template_name = 'student_list.html'
    context_object_name = 'students'


class StudentCreateView(CreateView):
    model = models.Student
    form_class = forms.StudentModelForm
    template_name = 'student_create.html'
    success_url = reverse_lazy('student_list')


class StudentDetailView(DetailView):
    model = models.Student
    template_name = 'student_detail.html'


class StudentUpdateView(UpdateView):
    model = models.Student
    form_class = forms.StudentModelForm
    template_name = 'student_update.html'
    success_url = reverse_lazy('student_list')


class StudentDeleteView(DeleteView):
    model = models.Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student_list')
