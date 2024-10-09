from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=50)
