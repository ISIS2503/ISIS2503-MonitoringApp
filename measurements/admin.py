from django.contrib import admin
from . models import Measurement, Variable, Threshold

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Variable)
admin.site.register(Threshold)
