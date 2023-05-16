from variables.models import Variable
from ..models import Measurement

def create_measurement(form):
    variable = None
    try:
        variable = Variable.objects.get(id=form["variable"])
    except:
        return False
    if(variable == None):
        return False
    else:
        measurement = Measurement()
        measurement.variable = variable
        measurement.value = form["value"]
        measurement.unit = form["unit"]
        measurement.place = form["place"]
        measurement.save()
        return True