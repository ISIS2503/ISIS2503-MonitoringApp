from django.db import models

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    

