from django.db import models

class Estudiante(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    age = models.IntegerField(null=True, blank=True)  # Edad
    course = models.CharField(max_length=100, null=True, blank=True)  # Curso

    def __str__(self):
        return f'{self.name} ({self.age} años)'
