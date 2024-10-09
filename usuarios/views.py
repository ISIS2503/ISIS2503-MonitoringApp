from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UsuarioForm 
from .logic.usuario_logic import get_usuarios, create_usuario 
def usuario_list(request):  
    usuarios = get_usuarios()  
    context = {
        'usuario_list': usuarios  
    }
    return render(request, 'Usuario/usuarios.html', context) 

def usuario_create(request):  
    if request.method == 'POST':
        form = UsuarioForm(request.POST)  
        if form.is_valid():
            create_usuario(form)  
            messages.add_message(request, messages.SUCCESS, 'Successfully created usuario')  
            return HttpResponseRedirect(reverse('usuarioCreate'))  
        else:
            print(form.errors)
    else:
        form = UsuarioForm()  

    context = {
        'form': form,
    }
    return render(request, 'Usuario/usuarioCreate.html', context)  
