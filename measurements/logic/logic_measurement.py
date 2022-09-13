from ..models import Measurement

def get_measurements():
    queryset = Measurement.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_measurement(form):
    measurement = form.save()
    measurement.save()
    return ()

def create_measurement_object(variable_id, value, unit, place):
    measurement = Measurement()
    measurement.variable = variable_id
    measurement.value = value
    measurement.unit = unit
    measurement.place = place
    measurement.save()
    return ()