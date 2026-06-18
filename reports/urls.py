from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('reports/', views.report_list),
    path('reportcreate/', csrf_exempt(views.report_create), name='reportCreate'),
]