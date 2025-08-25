from django import forms
from .models import Cronograma

class CronogramaForm(forms.ModelForm):
    class Meta:
        model = Cronograma
        fields = ['codigo', 'grado', 'costo', 'fecha_causacion', 'tipo_pago', 'curso']

        labels = {
            'codigo': 'codigo de cronograma',
            'grado': 'grado de estudiantes',
            'costo': 'costo de matricula',
            'fecha_causacion': 'fecha de pago',
            'tipo_pago': 'tipo de metodo de pago',
            'curso': 'cursos de los estudiantes',
        }
