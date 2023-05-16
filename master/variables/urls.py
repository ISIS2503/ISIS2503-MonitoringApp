from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('variablecreate/', csrf_exempt(views.variable_create), name='variableCreate'),
]