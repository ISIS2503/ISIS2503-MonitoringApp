
#HOla

from ..models import Cita

def get_citas(var_pk):
    queryset = Cita.objects.get(pk=var_pk)
    return queryset

def create_cita(form):
    cita = form.save()
    cita.save()
    return ()

