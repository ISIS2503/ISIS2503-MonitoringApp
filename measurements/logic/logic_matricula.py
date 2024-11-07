from ..models import Matricula

def get_matriculas():
    queryset = Matricula.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_matricula(form):
    matricula = form.save()
    matricula.save()
    return ()

# logic_matricula.py

def delete_matricula(matricula_id):
    # Lógica para eliminar una medición
    try:
        matricula = Matricula.objects.get(id=matricula_id)
        matricula.delete()
    except Matricula.DoesNotExist:
        raise ValueError("La medición no existe")
