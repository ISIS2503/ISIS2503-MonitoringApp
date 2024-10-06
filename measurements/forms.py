from django import forms
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            'variable',       # Estudiante
            'value',          # Precio de matrícula
            'unit',           # Curso
            'place',          # Institución o lugar de matrícula
            #'dateTime',      # Fecha de matrícula (mantener, pero desactivado)
        ]

        labels = {
            'variable': 'Estudiante',
            'value': 'Precio de Matrícula',
            'unit': 'Curso',
            'place': 'Lugar de Matrícula',
            #'dateTime': 'Fecha de Matrícula',
        }