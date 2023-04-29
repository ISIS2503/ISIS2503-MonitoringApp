from django.db import models
from historias.models import Historia
from plantillas.models import Plantilla

class Cita(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE, default=None)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE, default=None)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{"historia": %s}' % (self.historia.name)
    
    def toJson(self):
        cita = {
            'historia': self.historia.name,
            'historia': self.plantilla.nombre,
            'dateTime': self.dateTime,
        }
        return cita