"""
from ..models import Acompanante

def get_measurements():
    queryset = Measurement.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_acompanante(form):
    acompanante = form.save()
    acompanante.save()
    return ()
"""
