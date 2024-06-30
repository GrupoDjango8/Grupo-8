from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Cliente, Menu, Pedido, PedidoItem

#json

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    # objeto = Menu.objects.get(pk=id_obj)
    # objeto.delete()
    # objetos = Menu.objects.all()
    # return render(request,  "webGOcho/administracion.html", {"objetos_menu":objetos})
    objeto = get_object_or_404(Menu, pk=id_obj)
    objeto.delete()
    return redirect('administracion')
    
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

#acciones con cliente

def eliminar_cliente(request, id_obj):
    objeto = get_object_or_404(Cliente, pk=id_obj)
    objeto.delete()
    return redirect('administracion')

#Pedidos administración
@csrf_exempt
def enviar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numero_mesa = data.get('numeroMesa')
            precio_total = data.get('precioTotal')
            pedido = data.get('pedido')

            # Procesar el pedido aquí
            # Por ejemplo, guardar el pedido en la base de datos

            response_data = {
                'status': 'success',
                'message': 'Pedido recibido correctamente',
                'numeroMesa': numero_mesa,
                'precioTotal': precio_total,
                'pedido': pedido
            }
            #agregar pedido a la base:
            print('mesa',response_data['numeroMesa'], 'precio',response_data['precioTotal'], 'pedido:', response_data['pedido']) 
            nuevo_pedido = {
                'numero_mesa': response_data['numeroMesa'],
                'precio_total': response_data['precioTotal'],
                'estado': 'PENDIENTE',
                #'comida_bebida': response_data['pedido']
            }
            clientes = Cliente.objects.all()
            for cliente in clientes:
                #print(cliente.numero_mesa)
                if str(cliente.numero_mesa) == nuevo_pedido['numero_mesa']:
                    print('hola')
                    print(cliente)
                    nuevo_pedido['numero_mesa']=cliente
                else:
                    print('Cliente no encontrado')

            nuevo_pedido = Pedido(
                numero_mesa = nuevo_pedido['numero_mesa'],
                precio_total = nuevo_pedido['precio_total'],
                estado = nuevo_pedido['estado']
            )
            
            print(nuevo_pedido)
            nuevo_pedido.save()
            obj_menu = Menu.objects.all()
            array_mandar = []
            for i in range (len(response_data['pedido'])):
                for item in obj_menu:
                    if item.nombre_del_producto == response_data['pedido'][i]['nombre']:
                        print(item)
                        array_mandar.append({
                            'pedido': item,
                            'cantidad': response_data['pedido'][i]['cantidad'],
                            'precio': response_data['pedido'][i]['precio']* response_data['pedido'][i]['cantidad']
                        })
            print(array_mandar)
            for p in array_mandar:
                nuevo_pedido_item = PedidoItem(
                    pedido = nuevo_pedido,
                    menu = p['pedido'],
                    cantidad = p['cantidad'],
                )
                nuevo_pedido_item.save()
            #print(response_data['pedido'][0]['nombre'])

            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#Eliminar pedido Item
def eliminar_pedido(request, id_obj):
    #objeto = PedidoItem.objects.get(pk=id_obj)
    #objeto.delete()
    #objetos = PedidoItem.objects.all()
    #return render(request,  "webGOcho/administracion.html", {"objetos_pedido":objetos})

    objeto = get_object_or_404(PedidoItem, pk=id_obj)
    objeto.delete()
    return redirect('administracion')

#eliminar al cliente pedido
def eliminar_pedido_cliente(request, id_obj):
    #objeto = PedidoItem.objects.get(pk=id_obj)
    #objeto.delete()
    #objetos = PedidoItem.objects.all()
    #return render(request,  "webGOcho/administracion.html", {"objetos_pedido":objetos})

    objeto = get_object_or_404(Pedido, pk=id_obj)
    objeto.delete()
    return redirect('administracion')



def editar_pedido_cliente(request,id_ped):
    objeto = Pedido.objects.get(pk=id_ped)
    form = EditPedidoForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect('administracion') 
    return render(request, 'webGOcho/editar_pedido_cliente.html', {'objeto':objeto,'form':form})