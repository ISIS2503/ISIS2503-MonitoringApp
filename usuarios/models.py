from django.db import models
import random
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    correo = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    saldoTotal = random.randint(100000,1000000)
    saldoDeber = random.randint(100000,1000000)

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.edad)

