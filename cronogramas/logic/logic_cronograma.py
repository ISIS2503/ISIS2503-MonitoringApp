from ..models import Cronograma

def get_cronogramas():
    queryset = Cronograma.objects.all()
    return queryset

def create_cronograma(form):
    cronograma = form.save()
    cronograma.save()
    return cronograma

def delete_cronograma(cronograma_id):
    try:
        cronograma = Cronograma.objects.get(id=cronograma_id)
        cronograma.delete()
    except Cronograma.DoesNotExist:
        raise ValueError("El cronograma no existe")
