

from ..models import Historia

def get_historia_by_name(name):
    queryset = Historia.objects.get(name=name)
    return (queryset)

def get_historias():
    queryset = Historia.objects.all()
    return (queryset)

def create_historia(form):
    plantilla = form.save()
    plantilla.save()
    return ()
