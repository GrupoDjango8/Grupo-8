from django import forms
from django.core.exceptions import ValidationError

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


class AltaProductoForm(forms.Form):
    objeto = forms.CharField(label='Objeto', required=True)
    nombre_del_producto = forms.CharField(label='Nombre del producto',required=True)
    subtipo = forms.CharField(label='Tipo de comida/bebida',required=True)
    descripcion = forms.CharField(label='Descripción',required=True)
    precio = forms.IntegerField(label='Precio',required=True)

    def clean_objeto(self):
        if not self.cleaned_data["objeto"].isalpha():
            raise ValidationError("El objeto solo puede estar compuesto por letras")

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