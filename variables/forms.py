from django import forms
from .models import Variable


#TODO: llenar valores formulario
class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
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