from django.shortcuts import render
from . import metrics

def home(request):
    sales_student = metrics.get_sales_metric()
    total_student_level = metrics.get_students_metric()
    context = {
        'sales_student': sales_student,
        'total_student_level': total_student_level
    }
    return render (request, 'home.html', context)