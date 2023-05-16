from django.shortcuts import render
from .forms import MeasurementForm
from django.contrib import messages
from django.http import HttpResponse
from .logic.logic_measurement import create_measurement
import json

def measurement_create(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        measurement = create_measurement(data_json)
        if(measurement):
            return HttpResponse('Successfully created measurement')
        else:
           return HttpResponse('Error creating measurement, variable does not exist')
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)