from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import Producto, Carrito, CarritoItem
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
import json

def agregar_al_carrito(request, producto_id):
    if request.method == "POST":
        data = json.loads(request.body)
        cantidad = int(data.get("cantidad", 1))

        producto = get_object_or_404(Producto, pk=producto_id)

        print('cantidad---->', cantidad)
        
        if producto.cantidad < cantidad:
            return JsonResponse({"status": "error", "message": "Cantidad no disponible en inventario"}, status=400)

        if request.user.is_authenticated:
            carrito, creado = Carrito.objects.get_or_create(
                usuario=request.user,
                defaults={'fecha_expiracion': timezone.now() + timedelta(minutes=30)}
            )
        else:
            carrito_id = request.session.get('carrito_id')
            
            if carrito_id:
                carrito = Carrito.objects.filter(id=carrito_id).first()
            else:
                # Si no existe, crear uno nuevo y asociarlo con la sesión
                carrito = Carrito(fecha_expiracion=timezone.now() + timedelta(minutes=30))
                carrito.save()
                request.session['carrito_id'] = carrito.id  # Guardar el ID del carrito en la sesión

        # Crear o actualizar el item en el carrito
        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()

        # Descontar del inventario
        # producto.cantidad -= cantidad
        # producto.save()

        return JsonResponse({"status": "success", "message": "Producto agregado al carrito"}, status=200)
    
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)


def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        
        carrito_id = request.session.get('carrito_id')
        carrito_sesion = Carrito.objects.filter(id=carrito_id).first() if carrito_id else None

        if not carrito:
            if carrito_sesion:
                carrito_sesion.usuario = request.user
                carrito_sesion.save()
                carrito = carrito_sesion
            else:
                carrito = Carrito(usuario=request.user)
                carrito.save()
        else:
            if carrito_sesion:
                for item in CarritoItem.objects.filter(carrito=carrito_sesion):
                    # Buscar si el producto ya existe en el carrito del usuario
                    carrito_item = CarritoItem.objects.filter(carrito=carrito, producto=item.producto).first()
                    if carrito_item:
                        carrito_item.cantidad += item.cantidad
                        carrito_item.save()
                    else:
                        item.carrito = carrito
                        item.save()
                carrito_sesion.delete()

        # Limpiar carrito de la sesión
        if 'carrito_id' in request.session:
            del request.session['carrito_id']
    else:
        # Usuario no autenticado, manejar carrito de sesión
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
        else:
            carrito = Carrito()
            carrito.save()
            request.session['carrito_id'] = carrito.id

    carrito_items = CarritoItem.objects.filter(carrito=carrito)

    total = calculo(carrito_items)

    html_content = render_to_string(
        'carrito/carrito_item.html',
        {'carrito_items': carrito_items, 'total': total},
        request=request
    )

    return HttpResponse(html_content)


def calculo(carrito_items):
    total = 0
    total_item = 0
    for item in carrito_items:
        subtotal = item.cantidad * item.producto.precio
        descuento = (item.producto.descuento / 100) * subtotal
        total_item = subtotal - descuento
        total += total_item
    return total

def eliminar_del_carrito(request, producto_id):
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                carrito = Carrito.objects.filter(usuario=request.user).first()
            else:
                carrito_id = request.session.get('carrito_id')
                carrito = Carrito.objects.get(id=carrito_id) if carrito_id else None

            if not carrito:
                return JsonResponse({"status": "error", "message": "Carrito no encontrado"}, status=404)

            carrito_item = CarritoItem.objects.filter(carrito=carrito, producto_id=producto_id).first()
            if not carrito_item:
                return JsonResponse({"status": "error", "message": "Producto no encontrado en el carrito"}, status=404)

            # Recuperar el inventario
            # producto = carrito_item.producto
            # producto.cantidad += carrito_item.cantidad
            # producto.save()

            carrito_item.delete()  # Elimina el ítem del carrito
            return JsonResponse({"status": "success", "message": "Producto eliminado del carrito"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Acceso no autorizado"}, status=403)



def actualizar_cantidad_carrito(request, producto_id):
    if request.method == "POST":
        try:
            # Cargar datos JSON desde el cuerpo de la solicitud
            data = json.loads(request.body)

            cantidad = int(data.get("cantidad", 1))

            if cantidad < 1:
                return JsonResponse({"status": "error", "message": "Cantidad inválida"}, status=400)

            if request.user.is_authenticated:
                carrito = Carrito.objects.filter(usuario=request.user).first()
            else:
                carrito_id = request.session.get('carrito_id')
                carrito = Carrito.objects.get(id=carrito_id) if carrito_id else None

            if not carrito:
                return JsonResponse({"status": "error", "message": "Carrito no encontrado"}, status=404)

            carrito_item = CarritoItem.objects.filter(carrito=carrito, producto_id=producto_id).first()
            if not carrito_item:
                return JsonResponse({"status": "error", "message": "Producto no encontrado en el carrito"}, status=404)

            # Verifica el inventario disponible
            producto = carrito_item.producto
            if cantidad > producto.cantidad + carrito_item.cantidad:
                return JsonResponse({"status": "error", "message": "Cantidad no disponible en inventario"}, status=400)

            # Actualiza la cantidad en el carrito
            producto.cantidad += carrito_item.cantidad  # Revertir la cantidad actual
            carrito_item.cantidad = cantidad
            producto.cantidad -= cantidad  # Descontar la nueva cantidad
            producto.save()
            carrito_item.save()

            total = calculo(CarritoItem.objects.filter(carrito=carrito))
            return JsonResponse({"status": "success", "message": "Cantidad actualizada", "total": total}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Método no permitido o usuario no autenticado"}, status=403)
