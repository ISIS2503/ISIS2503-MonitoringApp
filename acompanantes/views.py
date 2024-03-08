from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AcompananteForm
from .logic.acompanante_logic import get_acompanante, create_acompanante

def acompanante_list(request):
    acompanantes = get_acompanante()
    context = {
        'acompanante_list': acompanantes
    }
    return render(request, 'Acompanante/acompanantes.html', context)

def acompanante_create(request):
    if request.method == 'POST':
        form = AcompananteForm(request.POST)
        if form.is_valid():
            create_acompanante(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created acompanante')
            return HttpResponseRedirect(reverse('acompananteCreate'))
        else:
            print(form.errors)
    else:
        form = AcompananteForm()

    context = {
        'form': form,
    }
    return render(request, 'Acompanante/acompananteCreate.html', context)
