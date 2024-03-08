
from django.db import models
"""
from estudianteEstrella.models import EstudianteEstrella
"""
class Acompanante(models.Model):

    nombre = models.CharField(max_length=50)
    
    edad = models.FloatField(null=True, blank=True, default=None)
    """
    estudiante = models.ForeignKey(EstudianteEstrella, on_delete=models.CASCADE, default=None)
    """
    def __str__(self):
        return '%s %s' % (self.edad, self.nombre)
