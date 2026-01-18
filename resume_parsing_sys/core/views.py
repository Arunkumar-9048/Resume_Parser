from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexTemplate(TemplateView):
    template_name= 'index.html'
    
class EmployeeTemplate(TemplateView):
    template_name = 'employee.html'