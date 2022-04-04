from django import forms
from .models import EstudianteEstrella

class EstudianteEstrellaForm(forms.ModelForm):
    class Meta:
        model = EstudianteEstrella
        fields = [
            'nombre',
            'edad',
        ]
        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
        }