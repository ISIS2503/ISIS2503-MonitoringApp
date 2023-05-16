from django.shortcuts import render
from django.http import HttpResponse
from .forms import VariableForm
from .logic.variable_logic import create_variable
import json

def variable_create(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        create_variable(data_json)
        return HttpResponse('Successfully created variable')
    else:
        form = VariableForm()

    context = {
        'form': form,
    }
    return render(request, 'Variable/variableCreate.html', context)