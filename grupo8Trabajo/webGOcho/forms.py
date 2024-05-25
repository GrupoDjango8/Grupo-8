from django import forms
from django.core.exceptions import ValidationError

class AltaClienteForm(forms.Form):
    nombre= forms.CharField(label='Nombre del cliente',required=True)
    apellido = forms.CharField(label='Apellido del cliente',required=True)
    dni = forms.IntegerField(label='DNI', required=True)
    email = forms.EmailField(label='Email', required=True)
    numero_mesa = forms.IntegerField(label='Escriba su número de mesa', required=True)

    def clean_nombre(self):
        if not self.cleaned_data["nombre"].isalpha():
            raise ValidationError("El nombre solo puede estar compuesto por letras")

        return self.cleaned_data["nombre"]
    
    def clean_apellido(self):
        if not self.cleaned_data["apellido"].isalpha():
            raise ValidationError("El apellido solo puede estar compuesto por letras")

        return self.cleaned_data["apellido"]
