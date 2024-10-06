from ..models import Measurement

def get_measurements():
    queryset = Measurement.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_measurement(form):
    measurement = form.save()
    measurement.save()
    return ()

# logic_measurement.py

def delete_measurement(measurement_id):
    # Lógica para eliminar una medición
    try:
        measurement = Measurement.objects.get(id=measurement_id)
        measurement.delete()
    except Measurement.DoesNotExist:
        raise ValueError("La medición no existe")
