from rest_framework import serializers
from . import models


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'variable', 'value', 'unit', 'place', 'time',)
        model = models.Measurement