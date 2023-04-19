from django.db import models
from dj_cqrs.mixins import MasterMixin
from variables.models import Variable

class Measurement(MasterMixin, models.Model):

    CQRS_ID = 'measurement_model'

    #id = models.IntegerField(primary_key=True)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, default=None)
    value = models.FloatField(null=True, blank=True, default=None)
    unit = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)