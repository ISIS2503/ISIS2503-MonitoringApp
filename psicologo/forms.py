from django import forms
from .models import Psicologo

class PsicologoForm(forms.ModelForm):
    class Meta:
        model = Psicologo
        fields = [
            'nombre',
            'edad',
        ]
        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
        }