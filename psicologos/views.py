from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import PsicologoForm
from .logic.psicologo_logic import get_psicologos, create_psicologo

def psicologo_list(request):
    psicologos = get_psicologos()
    context = {
        'psicologo_list': psicologos
    }
    return render(request, 'Psicologo/psicologos.html', context)

def psicologo_create(request):
    if request.method == 'POST':
        form = PsicologoForm(request.POST)
        if form.is_valid():
            create_psicologo(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created Psicologo')
            return HttpResponseRedirect(reverse('psicologoCreate'))
        else:
            print(form.errors)
    else:
        form = PsicologoForm()

    context = {
        'form': form,
    }
    return render(request, 'Psicologo/psicologoCreate.html', context)