from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre', 
            'edad',
            'correo',
            'contrasena'
        ]
        labels = {
            'nombre': 'Nombre',  
            'edad': 'Edad',    
            'correo': 'Correo',
            'contrasena': 'Contrasena'
        }
