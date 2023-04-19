from django import forms
from .models import Variable

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = [
            'name',
        ]
        labels = {
            'name': 'Name',
        }