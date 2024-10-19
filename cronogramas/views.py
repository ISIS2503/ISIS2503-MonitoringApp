from django.shortcuts import render, redirect
from .forms import CronogramaForm  # Cambia MeasurementForm por CronogramaForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_cronograma import create_cronograma, get_cronogramas, delete_cronograma  # Importa las funciones de cronogramas
from django.shortcuts import render, get_object_or_404
from .models import Cronograma


def cronograma_list(request):
    cronogramas = get_cronogramas()
    return render(request, 'Cronogramas/cronograma_list.html', {'cronogramas': cronogramas})

def cronograma_create(request):
    if request.method == 'POST':
        form = CronogramaForm(request.POST)
        if form.is_valid():
            create_cronograma(form)
            messages.success(request, 'Cronograma creado exitosamente.')
            return redirect('cronograma_list')
    else:
        form = CronogramaForm()
    return render(request, 'Cronogramas/cronograma_form.html', {'form': form})

def cronograma_delete(request, cronograma_id):
    try:
        delete_cronograma(cronograma_id)
        messages.success(request, 'Cronograma eliminado exitosamente.')
        return redirect('cronograma_list')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('cronograma_list')

def cronograma_detail(request, pk):
    cronograma = get_object_or_404(Cronograma, pk=pk)
    return render(request, 'Cronogramas/cronograma_detail.html', {'cronograma': cronograma})
