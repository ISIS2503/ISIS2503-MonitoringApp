from django.db import models
from usuarios.models import Usuario

class Reporte(models.Model):
    id_estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True)
    concepto_pago = models.CharField(max_length=50)
    valor_pagado = models.IntegerField(default=0)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True) 
    descuento_aplicado = models.IntegerField(default=0)
    saldo_pendiente = models.IntegerField(default=0)
