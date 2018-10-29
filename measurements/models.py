from django.db import models

# Create your models here.

class Variable(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.name)

class Measurement(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True, default=None)
    unit = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=False)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)

class Threshold(models.Model):
    thresholdMax = models.FloatField(null=True, blank=True, default=None)
    thresholdMin = models.FloatField(null=True, blank=True, default=None)
    variable = models.OneToOneField(Variable, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return '%s %s' % (self.thresholdMax, self.variable.name)
