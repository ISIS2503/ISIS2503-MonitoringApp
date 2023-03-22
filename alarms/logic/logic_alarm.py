from measurements.models import Measurement
from ..models import Alarm

def get_alarms():
    queryset = Alarm.objects.all().order_by('-dateTime')
    return (queryset)

def get_measurements_by_variable(variable):
    queryset = Measurement.objects.filter(variable=variable).order_by('-dateTime')[:10]
    return (queryset)

def create_alarm(variable, measurement, limitExceeded):
    alarm = Alarm()
    alarm.variable = variable
    alarm.measurement = measurement
    alarm.value = measurement.value
    alarm.limitExceeded = limitExceeded
    alarm.save()
    return alarm