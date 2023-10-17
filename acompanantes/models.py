
from django.db import models

class Acompanante(models.Model):

    nombre = models.CharField(max_length=50)
    edad = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '%s %s' % (self.edad, self.nombre)
