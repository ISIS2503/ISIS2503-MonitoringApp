from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    correo = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.edad)

