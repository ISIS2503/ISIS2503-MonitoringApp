from django.db import models
#from acompanantes.models import Acompanante
#from psicologo.models import Psicologo

class EstudianteEstrella(models.Model):

    nombre = models.CharField(max_length=50)
    edad = models.FloatField(null=True, blank=True, default=None)
    activo = models.BooleanField();
    #acompanante = models.ForeignKey(Acompanante, on_delete=models.CASCADE)
    #psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s %s %s' % (self.edad, self.nombre, self.activo)
