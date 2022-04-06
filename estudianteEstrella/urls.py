
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('estudiantesEstrella/', views.estudianteEstrella_list),
    path('estudianteEstrellacreate/', csrf_exempt(views.estudianteEstrella_create), name='estudianteEstrellaCreate'),
]

