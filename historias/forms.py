from django import forms
from .models import Historia

class HistoriaForm(forms.ModelForm):
    class Meta:
        model = Historia
        fields = [
            'name',
        ]
        labels = {
            'name': 'Name',
        }
