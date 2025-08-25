from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('estudiantes/', views.estudiante_list, name='estudianteList'),
    path('estudiantecreate/', csrf_exempt(views.estudiante_create), name='estudianteCreate'),
    path('estudiantes/morosos', views.morosos_list, name='lista_morosos'),
]