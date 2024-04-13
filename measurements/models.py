from django.db import models
from variables.models import Variable

class Measurement(models.Model):
    #variable = models.ForeignKey(Solicitud, on_delete=models.CASCADE, default=None)
    trabajo = models.CharField(max_length=50)
    ingresos = models.FloatField(null=True, blank=True, default=None)
    deudas = models.FloatField(null=True, blank=True, default=None)
    creditos = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)