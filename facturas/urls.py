from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.buscar_reportes, name='buscar_reportes'),
    path('facturas/generar-pdf/<int:id_estudiante>/<str:fecha_emision>/<str:concepto_pago>/', views.generar_pdf, name='generar_pdf')
]