from django.urls import path
from . import views

urlpatterns = [
    path('reportes/', views.inicio_reportes, name='inicio_reportes'),
    path('reporte-usuario/', views.reporte_usuario, name='reporte_usuario'),
]
