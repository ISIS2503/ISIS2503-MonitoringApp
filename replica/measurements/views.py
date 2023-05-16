from django.shortcuts import render
from .forms import MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .logic.logic_measurement import create_measurement, get_measurements

def measurement_list(request):
    measurements = get_measurements()
    context = list(measurements.values())
    return JsonResponse(context, safe=False)