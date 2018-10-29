from django import forms
from .models import Threshold


class ThresholdForm(forms.ModelForm):

    class Meta:
        model = Threshold
        fields = [
            'thresholdMax',
            'thresholdMin',
        ]
        labels = {
            'thresholdMax': 'Max. Threshold',
            'thresholdMin': 'Min. Threshold',
        }
        widgets = {
            'thresholdMax': forms.TextInput(attrs={'class':'form-control'}),
            'thresholdMin': forms.TextInput(attrs={'class':'form-control'}),
        }