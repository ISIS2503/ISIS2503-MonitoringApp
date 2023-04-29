from plantillas.models import Plantilla
from ..models import Cita

def get_citas():
    queryset = Cita.objects.all().order_by('-dateTime')
    return (queryset)

def get_plantillas_by_historia(historia):
    queryset = Plantilla.objects.filter(historia=historia).order_by('-dateTime')[:10]
    return (queryset)

def create_cita( historia, plantilla):
    cita = Cita()
    cita.historia = historia
    cita.plantilla = plantilla
    cita.save()
    return cita