from django.db import models

class Measurement(models.Model):
    trabajo = models.CharField(max_length=50, default='')
    ingresos = models.FloatField(null=True, blank=True, default=None)
    deudas = models.FloatField(null=True, blank=True, default=None)
    creditos = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '{}'.format(self.trabajo)