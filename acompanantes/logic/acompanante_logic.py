
#HOla

from ..models import Acompanante

def get_acompanante():
    acompanante = Acompanante.objects.all()
    return acompanante

def create_acompanante(form):
    acompanante = form.save()
    acompanante.save()
    return ()

