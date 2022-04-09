from rest_framework import serializers
from . import models


class CitaSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'psicologo', 'dateTime', 'plataforma',)
        model = models.Cita