from django import forms
from .models import Acompanante

class AcompananteForm(forms.ModelForm):
    class Meta:
        model = Acompanante
        fields = [
            'nombre',
            'edad',
        ]
        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
        }