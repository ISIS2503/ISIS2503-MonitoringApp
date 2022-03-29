""""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('acompanantes/', views.acompanante_list),
    path('acompanantecreate/', csrf_exempt(views.acompanante_create), name='acompananteCreate'),
]
"""
