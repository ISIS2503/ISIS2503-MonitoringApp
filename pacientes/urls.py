from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('pacientes/', views.paciente_list, name='pacienteList'),
    path('paciente/create/', csrf_exempt(views.paciente_create), name='pacienteCreate'),
    path('paciente/<int:paciente_id>/', views.paciente_detail, name='pacienteDetail'),
]