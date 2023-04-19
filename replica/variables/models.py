from django.db import models
from dj_cqrs.mixins import ReplicaMixin

class Variable(ReplicaMixin, models.Model):
    CQRS_ID = 'variable_model'

    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.name)

