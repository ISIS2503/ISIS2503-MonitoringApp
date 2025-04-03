from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'edad', 'direccion', 'telefono']
        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }