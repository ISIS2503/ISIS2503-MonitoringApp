
#HOlaa

from ..models import EstudianteEstrella

def get_estudianteEstrella():
    measurement = EstudianteEstrella.objects.all()
    return measurement

def create_estudianteEstrella(form):
    estudianteEstrella = form.save()
    estudianteEstrella.save()
    return ()

