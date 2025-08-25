
#HOla

from ..models import Cita

def get_citas():
    queryset = Cita.objects.all().order_by('-dateTime')[:10]
    return queryset

def create_cita(form):
    cita = form.save()
    cita.save()
    return ()

