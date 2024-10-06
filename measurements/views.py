from django.shortcuts import render
from .forms import MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_measurement import create_measurement, get_measurements

def measurement_list(request):
    measurements = get_measurements()  # Lista de matrículas
    context = {
        'measurement_list': measurements
    }
    return render(request, 'Measurement/measurements.html', context)

def measurement_create(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            create_measurement(form)  # Crear matrícula
            messages.add_message(request, messages.SUCCESS, 'Matrícula creada exitosamente')
            return HttpResponseRedirect(reverse('measurementCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)