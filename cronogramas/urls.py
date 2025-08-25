from django.urls import path
from . import views

urlpatterns = [
    path('', views.cronograma_list, name='cronograma_list'),  # Lista de cronogramas
    path('<int:pk>/', views.cronograma_detail, name='cronograma_detail'),  # Detalle del cronograma
    path('nuevo/', views.cronograma_create, name='cronograma_create'),  # Crear un cronograma
    path('delete/<int:cronograma_id>/', views.cronograma_delete, name='cronograma_delete'),
]
