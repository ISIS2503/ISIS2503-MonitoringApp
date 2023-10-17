from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CitaForm
from .logic.cita_logic import get_cita, create_cita

def cita_list(request):
    cita = get_cita()
    context = {
        'cita_list': cita
    }
    return render(request, 'Cita/cita.html', context)

def cita_create(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            create_cita(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created cita')
            return HttpResponseRedirect(reverse('citaCreate'))
        else:
            print(form.errors)
    else:
        form = CitaForm()

    context = {
        'form': form,
    }
    return render(request, 'Cita/citaCreate.html', context)
