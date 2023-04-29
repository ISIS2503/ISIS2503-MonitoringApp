from django.shortcuts import render
from .forms import PlantillaForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_plantilla import create_plantilla, get_plantillas

def plantilla_list(request):
    plantillas = get_plantillas()
    context = {
        'plantilla_list': plantillas
    }
    return render(request, 'Plantilla/plantillas.html', context)

def plantilla_create(request):
    if request.method == 'POST':
        form = PlantillaForm(request.POST)
        if form.is_valid():
            create_plantilla(form)
            messages.add_message(request, messages.SUCCESS, 'Plantilla create successful')
            return HttpResponseRedirect(reverse('plantillaCreate'))
        else:
            print(form.errors)
    else:
        form = PlantillaForm()

    context = {
        'form': form,
    }

    return render(request, 'Plantilla/plantillaCreate.html', context)
