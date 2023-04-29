from ..models import Plantilla

def get_plantillas():
    queryset = Plantilla.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_plantilla(form):
    plantilla = form.save()
    plantilla.save()
    return ()
