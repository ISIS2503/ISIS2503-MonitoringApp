from django.db import models
from dj_cqrs.mixins import ReplicaMixin
from variables.models import Variable

class Measurement(ReplicaMixin, models.Model):

    CQRS_ID = 'measurement_model'
    CQRS_CUSTOM_SERIALIZATION = True

    #id = models.IntegerField(primary_key=True)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, default=None)
    value = models.FloatField(null=True, blank=True, default=None)
    unit = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)
    
    @staticmethod
    def _handle_variable(mapped_data):
        variable = Variable.objects.get(pk=mapped_data)
        return variable
    
    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None, meta=None):
        print(mapped_data['variable'])
        variable = cls._handle_variable(mapped_data['variable'])
        return Measurement.objects.create(
            id=mapped_data['id'],
            variable=variable,
            value=mapped_data['value'],
            unit=mapped_data['unit'],
            place=mapped_data['place'],
            dateTime=mapped_data['dateTime'],
            cqrs_revision=mapped_data['cqrs_revision'],
            cqrs_updated=mapped_data['cqrs_updated'],
        )
    
    def cqrs_update(self, sync, mapped_data, previous_data=None, meta=None):
        variable = self._handle_variable(mapped_data['variable'])
        self.value = mapped_data['value']
        self.variable = variable
        self.value = mapped_data['value']
        self.unit = mapped_data['unit']
        self.place = mapped_data['place']
        self.dateTime = mapped_data['dateTime']
        self.cqrs_revision = mapped_data['cqrs_revision']
        self.cqrs_updated = mapped_data['cqrs_updated']
        self.save()
        return self