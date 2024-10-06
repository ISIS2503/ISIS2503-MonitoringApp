from django import forms
from .models import Variable

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
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
