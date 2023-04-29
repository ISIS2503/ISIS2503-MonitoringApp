from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('historias/', views.historia_list, name='historiaList'),
    path('historiacreate/', csrf_exempt(views.historia_create), name='historiaCreate'),
]