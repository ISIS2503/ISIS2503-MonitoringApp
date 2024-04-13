from rest_framework import serializers
from . import models


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'trabajo', 'ingresos', 'deudas', 'creditos',)
        model = models.Measurement