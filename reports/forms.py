from django import forms
from .models import  Reports

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = [
            'variable',
            'period',
            'service',
            'cost',
            #'created_at',
        ]

        labels = {
            'variable' : 'Variable',
            'period' : 'Period',
            'service' : 'Service',
            'cost' : 'Cost',
            #'created_at' : 'Created At',
    
        }
