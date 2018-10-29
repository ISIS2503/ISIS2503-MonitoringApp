from .models import Measurement, Threshold, Variable
from django.shortcuts import render, redirect
from .forms import ThresholdForm
from django.contrib.auth.decorators import login_required
import json, requests


def index(request):
    return render(request, 'index.html')

@login_required
def MeasurementList(request):
    queryset = Measurement.objects.all().order_by('-time')[:10]
    context = {
        'measurement_list': queryset
    }
    return render(request, 'Measurement/measurements.html', context)

@login_required
def ThresholdList(request):
    queryset = Threshold.objects.all()
    role = getRole(request)
    context = {
        'threshold_list': queryset,
        'role': role
    }
    print("role= ", role)
    return render(request, 'Threshold/thresholds.html', context)

@login_required
def ThresholdEdit(request, id_threshold):
    threshold = Threshold.objects.get(variable=id_threshold)
    varName = Variable.objects.get(id=id_threshold)
    if request.method == 'GET':
        form = ThresholdForm(instance=threshold)
    else:
        form =ThresholdForm(request.POST, instance=threshold)
        if form.is_valid():
            form.save()
        return redirect('thresholdList')
    role = getRole(request)
    return render(request, 'Threshold/thresholdEdit.html', {'form':form, 'variable':varName.name, 'role': role})
