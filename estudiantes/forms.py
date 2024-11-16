from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            'name',
            'birth_date',  # Fecha de nacimiento
            'age',         # Edad
            'course',      # Curso
        ]
        labels = {
            'name': 'Nombre',
            'birth_date': 'Fecha de nacimiento',
            'age': 'Edad',
            'course': 'Curso',
        }
