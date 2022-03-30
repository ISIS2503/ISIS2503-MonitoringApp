from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import VariableForm
from .logic.acompanante_logic import get_acompanante, create_acompanante

def variable_list(request):
    variables = get_acompanante()
    context = {
        'variable_list': variables
    }
    return render(request, 'Variable/variables.html', context)

def variable_create(request):
    if request.method == 'POST':
        form = VariableForm(request.POST)
        if form.is_valid():
            create_acompanante(form)
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
