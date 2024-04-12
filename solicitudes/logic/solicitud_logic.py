from ..models import Solicitud

def get_solicitudes():
    queryset = Solicitud.objects.all()
    return (queryset)

def create_solicitud(form):
    measurement = form.save()
    measurement.save()
    return ()