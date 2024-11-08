from django.db import models
from variables.models import Estudiante  # Estudiante

class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, default=None)  # Estudiante
    value = models.FloatField(null=True, blank=True, default=None)  # Precio de la matrícula
    unit = models.CharField(max_length=50)  # Curso
    place = models.CharField(max_length=50)  # Lugar de matrícula
    dateTime = models.DateTimeField(auto_now_add=True)  # Fecha de matrícula
    extra_payment = models.FloatField(null=True, blank=True, default=0.0)  # Pagos adicionales

    def __str__(self):
        return '%s - %s' % (self.estudiante.name, self.unit)  # Mostramos el estudiante y el curso
