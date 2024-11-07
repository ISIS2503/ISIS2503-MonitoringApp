from django.shortcuts import render
from .forms import MatriculaForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_matricula import create_matricula, get_matriculas, delete_matricula
from measurements.models import Matricula

def matricula_list(request):
    matriculas = get_matriculas()  # Lista de matrículas
    context = {
        'matricula_list': matriculas
    }
    return render(request, 'Matricula/matriculas.html', context)

def matricula_create(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            create_matricula(form)  # Crear matrícula
            messages.add_message(request, messages.SUCCESS, 'Matrícula creada exitosamente')
            return HttpResponseRedirect(reverse('matricula_list'))
        else:
            print(form.errors)
    else:
        form = MatriculaForm()

    context = {
        'form': form,
    }

    return render(request, 'Matricula/matriculaCreate.html', context)

def matricula_delete(request, id):
    # Obtener el objeto Matricula o devolver un 404 si no existe
    matricula = get_object_or_404(Matricula, id=id)
    
    # Eliminar la medición
    matricula.delete()
    
    # Mostrar un mensaje de éxito
    messages.success(request, 'La matrícula fue eliminada exitosamente.')
    
    # Redirigir a la lista de mediciones (o cualquier otra vista)
    return redirect('matricula_list')  # 'matriculaList' debe ser el nombre de la URL donde se redirige