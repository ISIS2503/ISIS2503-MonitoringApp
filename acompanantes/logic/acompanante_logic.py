
from ..models import Acompanante

def get_acompanante(var_pk):
    measurement = Acompanante.objects.get(pk=var_pk)
    return measurement

def create_acompanante(form):
    acompanante = form.save()
    acompanante.save()
    return ()

