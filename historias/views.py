from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import HistoriaForm
from .logic.historia_logic import get_historias, create_historia

def historia_list(request):
    historias = get_historias()
    context = {
        'historia_list': historias
    }
    return render(request, 'Historia/historias.html', context)

def historia_create(request):
    if request.method == 'POST':
        form = HistoriaForm(request.POST)
        if form.is_valid():
            create_historia(form)
            messages.add_message(request, messages.SUCCESS, 'Successfully created historia')
            return HttpResponseRedirect(reverse('historiaCreate'))
        else:
            print(form.errors)
    else:
        form = HistoriaForm()

    context = {
        'form': form,
    }
    return render(request, 'Historia/historiaCreate.html', context)
