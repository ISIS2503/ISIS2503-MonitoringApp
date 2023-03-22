from django.http import JsonResponse
from django.shortcuts import render

from variables.logic.variable_logic import get_variable_by_id
from .logic.logic_alarm import get_alarms, get_measurements_by_variable, create_alarm

def alarm_list(request):
    alarms = get_alarms()
    context = list(alarms.values())
    return JsonResponse(context, safe=False)

def generate_alarm(request, variable_id):
    variable = get_variable_by_id(variable_id)
    measurements = get_measurements_by_variable(variable_id)
    createAlarm = False
    upperMeasurement = None
    for measurement in measurements:
        if measurement.value >= 30:
            createAlarm = True
            upperMeasurement = measurement
    if createAlarm:
        alarm = create_alarm(variable, upperMeasurement, 30)
        return JsonResponse(alarm.toJson(), safe=False)
    else:
        return JsonResponse({'message': 'No alarm created'}, status=200)