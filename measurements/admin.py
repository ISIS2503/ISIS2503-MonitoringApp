from django.contrib import admin
from . models import Measurement, Variable

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Variable)
