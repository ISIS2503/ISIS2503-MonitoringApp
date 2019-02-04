from .models import Measurement, Variable
from django.shortcuts import render, redirect
from .forms import VariableForm, MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'index.html')

def MeasurementList(request):
    queryset = Measurement.objects.all().order_by('-dateTime')[:10]
    context = {
        'measurement_list': queryset
    }
    return render(request, 'Measurement/measurements.html', context)

def MeasurementCreate(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save()
            measurement.save()
            messages.add_message(request, messages.SUCCESS, 'Measurement create successful')
            return HttpResponseRedirect(reverse('measurementCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)

def VariableList(request):
    queryset = Variable.objects.all()
    context = {
        'variable_list': queryset
    }
    return render(request, 'Variable/variables.html', context)

def VariableCreate(request):
    if request.method == 'POST':
        form = VariableForm(request.POST)
        if form.is_valid():
            measurement = form.save()
            measurement.save()
            messages.add_message(request, messages.SUCCESS, 'Variable create successful')
            return HttpResponseRedirect(reverse('variableCreate'))
        else:
            print(form.errors)
    else:
        form = VariableForm()

    context = {
        'form': form,
    }

    return render(request, 'Variable/variableCreate.html', context)