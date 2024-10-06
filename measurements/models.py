from django.db import models
from variables.models import Variable  # Estudiante

class Measurement(models.Model):  # Mantiene el nombre Measurement
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, default=None)  # Estudiante
    value = models.FloatField(null=True, blank=True, default=None)  # Precio de la matrícula
    unit = models.CharField(max_length=50)  # Curso
    place = models.CharField(max_length=50)  # Lugar de matrícula
    dateTime = models.DateTimeField(auto_now_add=True)  # Fecha de matrícula

    def _str_(self):
        return '%s - %s' % (self.variable.name, self.unit)  # Mostramos el estudiante y el curso