from ..models import Estudiante

def get_estudiantes():
    queryset = Estudiante.objects.all()
    return (queryset)

def create_estudiante(form):
    measurement = form.save()
    measurement.save()
    return ()