from ..models import Estudiante

def get_estudiantes():
    queryset = Estudiante.objects.all()
    return (queryset)

def create_estudiante(form):
    measurement = form.save()
    measurement.save()
    return ()

def get_estudiante(id):
    try:
        estudiante = Estudiante.objects.get(id=id)
    except Estudiante.DoesNotExist:
        estudiante = None  # Manejar el caso si el estudiante no existe
    return estudiante