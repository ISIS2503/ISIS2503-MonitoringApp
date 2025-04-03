from ..models import Paciente

def get_pacientes():
    """
    Obtener todos los pacientes.
    """
    queryset = Paciente.objects.all()
    return (queryset)

def create_paciente(form):
    """
    Crea un paciente a partir de un form.
    """
    paciente = form.save()
    paciente.save()
    return paciente

def get_paciente_by_id(paciente_id):
    """
    Obtiene un paciente  paciente por su ID. Devuelve None si no existe.
    """
    try:
        return Paciente.objects.get(id=paciente_id)
    except Paciente.DoesNotExist:
        return None