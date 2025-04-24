from django.shortcuts import render, redirect
from .models import Producto, Categoria
from django.shortcuts import render, get_object_or_404

# Create your views here.


def home(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'productos': productos, 'categorias': categorias})


def productos_por_categoria(request, categoria):
    try:
        categoria_obj = Categoria.objects.get(nombre=categoria)
        productos = Producto.objects.filter(categoria=categoria_obj)
        categorias = Categoria.objects.all() 
    except Categoria.DoesNotExist:
        productos = Producto.objects.none() 
    return render(request, 'productos.html', {'productos': productos, 'categoria': categoria, 'categorias': categorias})

def contacto(request):
    return render(request, 'contacto.html')

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all()
    return render(request, 'producto.html', {'producto': producto, 'categorias': categorias})

