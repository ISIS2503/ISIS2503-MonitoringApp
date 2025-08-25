from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import EstudianteEstrellaForm
from .logic.estudianteEstrella_logic import get_estudianteEstrella, create_estudianteEstrella

def estudianteEstrella_list(request):
    estudiantesEstrella = get_estudianteEstrella()
    context = {
        'estudianteEstrella_list': estudiantesEstrella
    }
    return render(request, 'EstudianteEstrella/estudiantesEstrella.html', context)

def estudianteEstrella_create(request):
    if request.method == 'POST':
        form = EstudianteEstrellaForm(request.POST)
        if form.is_valid():
            create_estudianteEstrella(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created acompanante')
            return HttpResponseRedirect(reverse('estudianteEstrellaCreate'))
        else:
            print(form.errors)
    else:
        form = EstudianteEstrellaForm()

    context = {
        'form': form,
    }
    return render(request, 'EstudianteEstrella/estudianteEstrellaCreate.html', context)
