from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import timedelta
from productos.models import Producto


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Permitir null en usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(default=timezone.now() + timedelta(minutes=30)) # Expira en 30 minutos

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ['carrito', 'producto']  # Para evitar duplicados en el carrito

    # Redefinimos el método save para ajustar la cantidad
    def save(self, *args, **kwargs):
        # Descontar del inventario al agregar al carrito
        if not self.pk:  # Solo si es un nuevo CarritoItem
            producto = self.producto
            if producto.cantidad >= self.cantidad:
                print('modifica cantidad')
                producto.cantidad -= self.cantidad
                producto.save()
            else:
                raise ValueError("Cantidad no disponible en inventario")
        super().save(*args, **kwargs)

# Ajustar cantidad al eliminar un CarritoItem
@receiver(post_delete, sender=CarritoItem)
def recuperar_inventario(sender, instance, **kwargs):
    print('recuperar inventario')
    producto = instance.producto
    producto.cantidad += instance.cantidad
    producto.save()
