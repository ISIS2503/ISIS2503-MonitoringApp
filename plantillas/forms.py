from django import forms
from .models import Plantilla

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = [
            'historia',
            'nombre',
            'especificacion',
            #'dateTime',
        ]

        labels = {
            'historia' : 'Historia',
            'nombre' : 'Nombre',
            'especificacion' : 'Especificacion',
            #'dateTime' : 'Date Time',
        }

