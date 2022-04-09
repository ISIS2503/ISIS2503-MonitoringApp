from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'pscilogo',
            'dateTime',
            'plataforma',   
        ]
        labels = {
            'psicologo': 'Psicologo',
            'dateTime': 'DateTime',
            'plataforma': 'Plataforma',
        }