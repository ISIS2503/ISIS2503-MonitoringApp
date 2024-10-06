from django.urls import path
from . import views

urlpatterns = [
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurement/create/', views.measurement_create, name='measurement_create'),
    path('measurement/<int:id>/delete/', views.measurement_delete, name='measurement_delete'),
]
