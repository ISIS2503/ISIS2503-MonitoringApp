from django.db import models

# Create your models here. hola
from psicologo.models import Psicologo
from acompanantes.models import Acompanante
from estudianteEstrella.models import EstudianteEstrella



class Cita(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, default=None)
    acompanantes = models.ForeignKey(Acompanante, on_delete=models.CASCADE, default=None)  
    estudianteEstrella = models.ForeignKey(EstudianteEstrella, on_delete=models.CASCADE, default=None)
    dateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    plataforma = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.dateTime, self.plataforma)