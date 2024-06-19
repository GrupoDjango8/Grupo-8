from django.contrib import admin

# Register your models here.
from .models import Cliente, Menu, Pedido, PedidoItem, AdministradorNegocio

admin.site.register(Cliente)
admin.site.register(Menu)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(AdministradorNegocio)