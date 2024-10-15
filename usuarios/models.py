from django.db import models
from cursos.models import Curso
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(null=True,max_length=50)
    edad = models.IntegerField()
    correo = models.CharField(max_length=50,default='correo@gmail.com')
    contrasena = models.CharField(max_length=50,default='1234')
    tipoUsuario = models.CharField(max_length=50,default='estudiante')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.edad)

