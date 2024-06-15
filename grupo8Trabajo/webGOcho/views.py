from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from .models import Cliente
# Create your views here.
#Renderizado del index
def index(request):
    contexto = {
        'bebidas':[
            ['Gaseosa',2000],
            ['Vino', 3000],
            ['Cerveza', 1500]
        ]
    }
    return render(request, "webGOcho/index.html", contexto)

#Renderizado del registro
def registro(request):
    contexto = {
        'alta_cliente': AltaClienteForm()
    }

    if request.method == "GET":
        contexto['alta_cliente'] = AltaClienteForm()
    
    else: # Asumo que es un POST
        form = AltaClienteForm(request.POST)
        contexto['alta_cliente'] = form
        
        # Validar el form
        if form.is_valid():
            # Si el form es correcto
            # Lo redirijo a una vista segura por ejemplo el index
            nuevo_cliente = Cliente(
                nombre = form.cleaned_data['nombre'], 
                apellido = form.cleaned_data['apellido'], 
                dni = form.cleaned_data['dni'], 
                email = form.cleaned_data['email'],
                numero_mesa = form.cleaned_data['numero_mesa']
            )
            nuevo_cliente.save()
            messages.success(request, 'El cliente fue dado de alta con éxito')
            return redirect('index')

        # Si el form es incorrecto
        # Se renderiza un form con mensajes de error  

    return render(request, "webGOcho/registro.html", contexto)