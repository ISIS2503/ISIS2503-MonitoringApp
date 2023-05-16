from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import VariableForm
from .logic.variable_logic import get_variables, create_variable

def variable_list(request):
    variables = get_variables()
    context = list(variables.values())
    return JsonResponse(context, safe=False)