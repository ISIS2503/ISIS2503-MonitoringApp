
#HOla

from ..models import Acompanante

def get_acompanante():
    measurement = Acompanante.objects.all()
    return measurement

def create_acompanante(form):
    acompanante = form.save()
    acompanante.save()
    return ()

