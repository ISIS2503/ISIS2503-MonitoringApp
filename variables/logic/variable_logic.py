from ..models import Variable

def get_variables():
    queryset = Variable.objects.all()
    return (queryset)

def get_variable_by_id(id):
    queryset = Variable.objects.get(id=id)
    return (queryset)

def create_variable(form):
    measurement = form.save()
    measurement.save()
    return ()