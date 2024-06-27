from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Cliente, Menu, Pedido, PedidoItem
# Create your views here.

#Renderizado del index
def index(request):
    # Hay que harcodear esto
    menu = Menu.objects.all()
    contexto = {
        'objetos_menu': menu,
        'mesas':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    }
    #print(contexto['objetos_menu'])
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


def user_logout(request):
    logout(request)
    messages.success(request, 'Sesion Cerrada')
    return(redirect('index'))


#Acá administra el administrador 
@login_required
def administracion(request):
    menu = Menu.objects.all()
    clientes = Cliente.objects.all()
    pedidos = PedidoItem.objects.all()
    pedidos_cliente = Pedido.objects.all()
    contexto = {
        'objetos_menu': menu,
        'clientes': clientes,
        'pedidos': pedidos,
        'pedidos_cliente': pedidos_cliente
    }
    return render(request, "webGOcho/administracion.html", contexto)

def alta_producto(request):
    contexto = {
        'alta_producto': AltaProductoForm()
    }

    if request.method == "GET":
        contexto['alta_producto'] = AltaProductoForm()
    
    else: # Asumo que es un POST
        form = AltaProductoForm(request.POST)
        contexto['alta_producto'] = form
        
        # Validar el form
        if form.is_valid():
            # Si el form es correcto
            # Lo redirijo a una vista segura por ejemplo el index
            nuevo_producto = Menu(
                objeto = form.cleaned_data['objeto'],
                nombre_del_producto = form.cleaned_data['nombre_del_producto'],
                subtipo = form.cleaned_data['subtipo'],
                descripcion = form.cleaned_data['descripcion'],
                precio = form.cleaned_data['precio'],
            )
            nuevo_producto.save()
            messages.success(request, 'El producto fue dado de alta con éxito')
            return redirect('administracion')

        # Si el form es incorrecto
        # Se renderiza un form con mensajes de error  

    return render(request, "webGOcho/alta_producto.html", contexto)


#Eliminar un producto
def eliminar(request, id_obj):
    objeto = Menu.objects.get(pk=id_obj)
    objeto.delete()
    objetos = Menu.objects.all()
    return render(request,  "webGOcho/administracion.html", {"objetos_menu":objetos})

#editar producto
def editar_producto(request,id_menu):
    objeto = Menu.objects.get(pk=id_menu)
    form = AltaProductoForm(request.POST or None, instance=objeto)
    if form.is_valid():
        """ nuevo_producto = Menu(
                objeto = form.cleaned_data['objeto'],
                nombre_del_producto = form.cleaned_data['nombre_del_producto'],
                subtipo = form.cleaned_data['subtipo'],
                descripcion = form.cleaned_data['descripcion'],
                precio = form.cleaned_data['precio'],
        )
        nuevo_producto.save() """
        form.save()
        return redirect('administracion')
    return render(request, 'webGOcho/edicion_producto.html', {'objeto':objeto,'form':form})

def eliminar_cliente(request, id_obj):
    objeto = Cliente.objects.get(pk=id_obj)
    objeto.delete()
    clientes = Cliente.objects.all()
    return render(request,  "webGOcho/administracion.html", {"clientes":clientes})


