from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=250)
    precio = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    descuento = models.DecimalField(default=None, max_digits=10, decimal_places=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0) 
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre


class Configuracion(models.Model):
    nombre_empresa = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    redes_sociales = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre_empresa
