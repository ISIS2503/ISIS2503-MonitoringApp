from ..models import Variable

def create_variable(form):
    variable = Variable()
    variable = Variable()
    variable.name = form["name"]
    variable.save()
    return variable