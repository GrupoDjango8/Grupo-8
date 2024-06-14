from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

##Cliente:               
#Nombre 
#Apellido
#Dni
#Email
#Numero_mesa 

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.IntegerField(verbose_name="DNI", unique=True)
    email = models.EmailField(verbose_name='Email')
    numero_mesa = models.IntegerField(verbose_name='Numero de mesa', unique=True,
         validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ]                            
    )

# Menú: 
#   Objeto:      Comidas ó Bebidas
#   Nombre producto: Plato
#   SubTipo:             (Tipo Bebida/Tipo Bebida) 
#   Descripción:       (Tipo Bebida/Tipo Bebida)                  
#   Precio:
class Menu(models.Model):
    objeto = models.CharField(verbose_name='Objeto')
    nombre_del_producto = models.CharField(verbose_name='Nombre del producto')
    subtipo = models.CharField(verbose_name='Tipo de comida/bebida')
    descripcion = models.CharField(verbose_name='Descripción')
    precio = models.IntegerField(verbose_name='Precio')

# hola = 'hola'
#Pedido
#FK MESA
#Precio total
#observaciones
#pedido Comida/Bebida y cantidad
# class Pedido(models.Model):
#     numero_mesa = models.ForeignKey(Cliente, verbose_name= 'Numero de mesa',on_delete=models.CASCADE, blank=True)
#     precio_total = models.IntegerField(verbose_name='Precio total')
#     observaciones = models.TextField(verbose_name='Observaciones')
#     estado_pedido = models.CharField(max_length=50, verbose_name="Estado del pedido", choices=[
#        ("Pendiente", "Pending"),
 ##      ("Completado", "Completed"),
   #     ], default="Pendiente")
#     comida_bebida = models.ManyToManyField(Menu,through='Pedido items y cantidad') #-> Este me tira error
#     items_pedido = models.ManyToManyField(Menu, through='PedidoItems') #-> esto lo agrega gemini

#Pedido según chat gpt
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENTREGADO', 'Entregado'),
    ]
    
    numero_mesa = models.ForeignKey(Cliente, verbose_name='Numero de mesa', on_delete=models.CASCADE, blank=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio total')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name='Estado del pedido')
    comida_bebida = models.ManyToManyField(Menu, through='PedidoItem')

    def calcular_precio_total(self):
        total = 0
        for item in self.pedidoitem_set.all():
            total += item.menu.precio * item.cantidad
        self.precio_total = total
        self.save()

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)


    