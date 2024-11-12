from rest_framework import serializers
from . import models

class MatriculaSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'variable', 'value', 'unit', 'place', 'dateTime',)  # Adaptado para matrícula
        model = models.Matricula