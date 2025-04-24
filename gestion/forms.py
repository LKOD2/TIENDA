
from django import forms
from productos.models import Producto, Configuracion, Categoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get('precio')
        descuento = cleaned_data.get('descuento')

        # Validar que el precio no sea negativo
        if precio is not None and precio < 0:
            self.add_error('precio', 'El precio no puede ser negativo.')
        
        # Validar que el descuento esté entre 0 y 100
        if descuento is not None and (descuento < 0 or descuento > 100):
            self.add_error('descuento', 'El descuento debe estar entre 0 y 100.')

        return cleaned_data
   

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['nombre_empresa', 'logo', 'direccion', 'telefono', 'email_contacto', 'redes_sociales']

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico')
    # imagen = forms.ImageField(label='imagen')


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': 'Nombre de usuario'}
