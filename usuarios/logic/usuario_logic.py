from ..models import Usuario

def get_usuarios():
    queryset = Usuario.objects.all()
    return (queryset)

def create_usuario(form):
    measurement = form.save()
    measurement.save()
    return ()