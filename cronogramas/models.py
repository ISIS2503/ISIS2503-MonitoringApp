from django.db import models
from variables.models import Variable  # Estudiante
import json

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    estudiantes = models.ManyToManyField(Variable, related_name='cursos')  # Reemplazamos 'Estudiante' por 'Variable'

    def _str_(self):
        return self.nombre

class Cronograma(models.Model):
    codigo = models.IntegerField(unique=True)
    grado = models.TextField()  # Usamos TextField para almacenar la lista de grados como un string
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_causacion = models.DateField(null=True, blank=True)
    tipo_pago = models.CharField(max_length=50, choices=[('transferencia', 'Transferencia'), ('efectivo', 'Efectivo')])
    curso = models.CharField(max_length=100)

    def _str_(self):
        return f'Cronograma {self.codigo} - {self.curso.nombre}'

    # Métodos para manejar la conversión de JSON a string y viceversa
    def set_grado(self, grado):
        """Convierte una lista de grados a JSON string y lo guarda en el campo grado"""
        self.grado = json.dumps(grado)

    def get_grado(self):
        """Convierte el campo grado de JSON string a una lista de grados"""
        return json.loads(self.grado)