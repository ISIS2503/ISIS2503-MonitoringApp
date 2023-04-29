from django.db import models
from historias.models import Historia

class Plantilla(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=50)
    especificacion = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.especificacion)
