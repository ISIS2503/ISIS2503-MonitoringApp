from django.db import models
from variables.models import Variable

class Reports(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, default=None)
    period = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=18, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.project_id, self.period, self.service)