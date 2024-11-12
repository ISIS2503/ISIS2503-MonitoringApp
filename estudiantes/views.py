from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Estudiante  # Asegúrate de importar el modelo Estudiante
from matriculas.models import Matricula
from django.contrib.auth.decorators import login_required

from .forms import EstudianteForm
from .logic.estudiante_logic import get_estudiantes, create_estudiante

def morosos_list(request):
    # Precio de la matrícula
    precio_matricula = 1000000

    # Obtener la lista de estudiantes y sus cuentas
    estudiantes = Estudiante.objects.all()
    cuentas = Matricula.objects.all()

    # Lista para almacenar los estudiantes que deben dinero
    morosos = []

    # Calcular la deuda de cada estudiante
    for estudiante in estudiantes:
        cuentas_estudiante = cuentas.filter(estudiante=estudiante)
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

    return render(request, 'Estudiante/morosos_list.html', context)

def estudiante_list(request):
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    if query:
        estudiantes = Estudiante.objects.filter(name__icontains=query)  # Filtrar por nombre
    else:
        estudiantes = get_estudiantes()  # Obtener todas si no hay búsqueda

    context = {
        'estudiante_list': estudiantes,
        'search_query': query  # Pasar la consulta al contexto para mantenerla en el formulario
    }
    return render(request, 'Estudiante/estudiantes.html', context)

def estudiante_create(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            create_estudiante(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created estudiante')
            return HttpResponseRedirect(reverse('estudianteCreate'))
        else:
            print(form.errors)
    else:
        form = EstudianteForm()

    context = {
        'form': form,
    }
    return render(request, 'Estudiante/estudianteCreate.html', context)

