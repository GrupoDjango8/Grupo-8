from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#Renderizado del index
def index(request):
    return render(request, "webGOcho/index.html")

#Renderizado del registro
def registro(request):
    return render(request, "webGOcho/registro.html")