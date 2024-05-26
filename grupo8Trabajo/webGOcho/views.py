from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import AltaClienteForm

# Create your views here.
#Renderizado del index
def index(request):
    return render(request, "webGOcho/index.html")

#Renderizado del registro
def registro(request):
    contexto = {
        'alta_cliente': AltaClienteForm()
    }
    return render(request, "webGOcho/registro.html", contexto)

