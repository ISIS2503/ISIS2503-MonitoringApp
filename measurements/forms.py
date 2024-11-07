from django import forms
from .models import Matricula

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = [
            'variable',       # Estudiante
            'value',          # Precio de matrícula
            'unit',           # Curso
            'place',          # Institución o lugar de matrícula
            'extra_payment',  # Pagos extras
        ]

        labels = {
            'variable': 'Estudiante',
            'value': 'Precio de Matrícula',
            'unit': 'Curso',
            'place': 'Lugar de Matrícula',
            'extra_payment': 'Pago Extra',
        }
