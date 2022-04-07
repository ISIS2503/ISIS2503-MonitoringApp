
#HOla

from ..models import Psicologo

def get_variables():
    queryset = Psicologo.objects.all()
    return (queryset)

def create_cita(form):
    cita = form.save()
    cita.save()
    return ()

