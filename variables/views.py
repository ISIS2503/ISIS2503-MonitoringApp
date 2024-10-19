from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Variable  # Asegúrate de importar el modelo Variable
from measurements.models import Measurement

from .forms import VariableForm
from .logic.variable_logic import get_variables, create_variable

def morosos_list(request):
    # Precio de la matrícula
    precio_matricula = 1000000

    # Obtener la lista de estudiantes y sus cuentas
    estudiantes = Variable.objects.all()
    cuentas = Measurement.objects.all()

    # Lista para almacenar los estudiantes que deben dinero
    morosos = []

    # Calcular la deuda de cada estudiante
    for estudiante in estudiantes:
        cuentas_estudiante = cuentas.filter(variable=estudiante)
        total_pagado = sum(cuenta.value for cuenta in cuentas_estudiante)
        deuda = precio_matricula - total_pagado

        if deuda > 0:
            morosos.append({
                'estudiante': estudiante,
                'deuda': deuda,
            })

    context = {
        'morosos': morosos
    }

    return render(request, 'Variable/morosos_list.html', context)

def variable_list(request):
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    if query:
        variables = Variable.objects.filter(name__icontains=query)  # Filtrar por nombre
    else:
        variables = get_variables()  # Obtener todas si no hay búsqueda

    context = {
        'variable_list': variables,
        'search_query': query  # Pasar la consulta al contexto para mantenerla en el formulario
    }
    return render(request, 'Variable/variables.html', context)

def variable_create(request):
    if request.method == 'POST':
        form = VariableForm(request.POST)
        if form.is_valid():
            create_variable(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created variable')
            return HttpResponseRedirect(reverse('variableCreate'))
        else:
            print(form.errors)
    else:
        form = VariableForm()

    context = {
        'form': form,
    }
    return render(request, 'Variable/variableCreate.html', context)

