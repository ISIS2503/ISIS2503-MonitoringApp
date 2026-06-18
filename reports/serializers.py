from rest_framework import serializers
from . import models


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'variable', 'period', 'service', 'cost','created_at',)
        model = models.Reports