from rest_framework import serializers
from . import models


class PlantillaSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'historia', 'nombre', 'especificacion', 'time',)
        model = models.Plantilla
