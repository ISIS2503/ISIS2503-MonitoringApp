from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import PacienteForm
from .logic.paciente_logic import get_pacientes, create_paciente, get_paciente_by_id

def paciente_list(request):
    pacientes = get_pacientes()
    return render(request, 'pacientes/pacientes.html', {'paciente_list': pacientes})

def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            create_paciente(form)
            messages.success(request, 'Paciente creado con éxito')
            return redirect('pacienteList')
    else:
        form = PacienteForm()
    
    return render(request, 'pacientes/pacienteCreate.html', {'form': form})

def paciente_detail(request, paciente_id):
    paciente = get_paciente_by_id(paciente_id)
    if not paciente:
        messages.error(request, "El paciente no existe")
        return redirect('pacienteList')

    return render(request, 'pacientes/paciente_detail.html', {'paciente': paciente})
