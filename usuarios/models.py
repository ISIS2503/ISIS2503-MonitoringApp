from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.edad)

