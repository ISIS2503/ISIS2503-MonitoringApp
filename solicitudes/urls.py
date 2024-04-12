from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('solicitudes/', views.solicitud_list, name='solicitudList'),
    path('solicitudcreate/', csrf_exempt(views.solicitud_create), name='solicitudCreate'),
]