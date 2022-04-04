from django.db import models

# Create your models here.
# tienes que poner los one to many de psicologo y companante

class EstudianteEstrella(models.Model):

    nombre = models.CharField(max_length=50)
    edad = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '%s %s' % (self.edad, self.nombre)
