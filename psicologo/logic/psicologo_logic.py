
#HOla

from ..models import Psicologo

def get_psicologo():
    queryset = Psicologo.objects.all()
    return (queryset)

def create_psicologo(form):
    cita = form.save()
    cita.save()
    return ()

