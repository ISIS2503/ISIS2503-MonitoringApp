from django import forms
from .models import Solicitud


#TODO: llenar valores formulario
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'name',
            'lastname',
            'country',
            'city',
            'phone',
            'mail'
        ]
        labels = {
            'name': 'Name',
            'lastname': 'Lastname',
            'country': 'Country',
            'city': 'City',
            'phone': 'Phone',
            'mail': 'Mail'
        }