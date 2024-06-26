from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Menu, Pedido
class AltaClienteForm(forms.Form):
    nombre= forms.CharField(label='Nombre del cliente',required=True)
    apellido = forms.CharField(label='Apellido del cliente',required=True)
    dni = forms.IntegerField(label='DNI', required=True)
    email = forms.EmailField(label='Email', required=True)
    #telefono = forms.IntegerField(label='Número de telefono', required=True)
    numero_mesa = forms.IntegerField(label='Escriba su número de mesa', required=True)

    def clean_nombre(self):
        if not self.cleaned_data["nombre"].isalpha():
            raise ValidationError("El nombre solo puede estar compuesto por letras")

        return self.cleaned_data["nombre"]
    
    def clean_apellido(self):
        if not self.cleaned_data["apellido"].isalpha():
            raise ValidationError("El apellido solo puede estar compuesto por letras")

        return self.cleaned_data["apellido"]

    def clean_dni(self):
        if not isinstance(self.cleaned_data["dni"], int):
            raise ValidationError("El apellido solo puede estar compuesto por letras")

        return self.cleaned_data["dni"]

    def clean_numero_mesa(self):
        clientes = Cliente.objects.all()
        for cliente in clientes:
            if int(cliente.numero_mesa) == int(self.cleaned_data["numero_mesa"]):
                raise ValidationError("El número está ocupado")
        return self.cleaned_data["numero_mesa"]
    
class AltaProductoForm(forms.Form):
    objeto = forms.CharField(label='Objeto', required=True)
    nombre_del_producto = forms.CharField(label='Nombre del producto',required=True)
    subtipo = forms.CharField(label='Tipo de comida/bebida',required=True)
    descripcion = forms.CharField(label='Descripción',required=True)
    precio = forms.IntegerField(label='Precio',required=True)

     
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(AltaProductoForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['objeto'].initial = self.instance.objeto
            self.fields['nombre_del_producto'].initial = self.instance.nombre_del_producto
            self.fields['subtipo'].initial = self.instance.subtipo
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['precio'].initial = self.instance.precio


    def clean_objeto(self):
        if not self.cleaned_data["objeto"].isalpha():
            raise ValidationError("El objeto solo puede estar compuesto por letras")
        if self.cleaned_data["objeto"] != 'comida'and self.cleaned_data["objeto"] != 'Comida' and self.cleaned_data["objeto"] != 'Bebida' and self.cleaned_data["objeto"] != 'bebida':
            raise ValidationError("El objeto debe ser comida o bebida")
        return self.cleaned_data["objeto"]
    
    def clean_subtipo(self):
        if not self.cleaned_data["subtipo"].isalpha():
            raise ValidationError("El tipo de comida/bebida solo puede contener letras y números")

        return self.cleaned_data["subtipo"]


    def clean_precio(self):
        if not isinstance(self.cleaned_data["precio"], int):
            raise ValidationError("El precio debe ser un número")
        
        if self.cleaned_data["precio"] <= 0:
            raise ValidationError("El precio debe ser un número mayor que 0")
        
        return self.cleaned_data["precio"]

    def save(self, commit=True):
        if self.instance:
            self.instance.objeto = self.cleaned_data['objeto']
            self.instance.nombre_del_producto = self.cleaned_data['nombre_del_producto']
            self.instance.subtipo = self.cleaned_data['subtipo']
            self.instance.descripcion = self.cleaned_data['descripcion']
            self.instance.precio = self.cleaned_data['precio']
            if commit:
                self.instance.save()
        return self.instance
    

class EditPedidoForm(forms.Form):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENTREGADO', 'Entregado'),
    ]
    
    numero_mesa = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Número de mesa',
        required=True
    )
    precio_total = forms.IntegerField(label='Precio Total', required=True)
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado', required=True)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(EditPedidoForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['numero_mesa'].initial = self.instance.numero_mesa
            self.fields['precio_total'].initial = self.instance.precio_total
            self.fields['estado'].initial = self.instance.estado

    def save(self, commit=True):
        if self.instance:
            self.instance.numero_mesa = self.cleaned_data['numero_mesa']
            self.instance.precio_total = self.cleaned_data['precio_total']
            self.instance.estado = self.cleaned_data['estado']
            if commit:
                self.instance.save()
        return self.instance
    