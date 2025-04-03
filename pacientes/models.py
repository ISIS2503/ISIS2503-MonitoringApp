from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.nombre} ({self.edad} años)"


