
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductoForm 
from django.db.models import Q 
from gestion.forms import ConfiguracionForm, CategoriaForm, UsuarioForm
from productos.models import Producto, Configuracion, Categoria
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

# Función para verificar que el usuario es superusuario o staff
def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_superuser_or_staff)
@login_required
def gestion_home(request):
    return render(request, 'gestion/inicio.html')

# -------- PRODUCTOS ----------

@user_passes_test(is_superuser_or_staff)
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'gestion/lista_productos.html', {'productos': productos})

@user_passes_test(is_superuser_or_staff)
@login_required
def buscar_productos(request):
    query = request.GET.get('query')
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(marca__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    return render(request, 'gestion/lista_productos.html', {'productos': productos, 'query': query})

@user_passes_test(is_superuser_or_staff)
@login_required
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, "Producto agregado")
            return redirect('lista_productos')
        else:
            print('Formulario no válido')
    else:
        form = ProductoForm()
    return render(request, 'gestion/form_producto.html', {'form': form})

@user_passes_test(is_superuser_or_staff)
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.error(request, "Producto editado")
            return redirect('lista_productos')
        else:
            print("Formulario no válido")
            print(form.errors)
    else:

        form = ProductoForm(instance=producto)
    
    return render(request, 'gestion/form_producto.html', {'form': form, 'producto': producto})

@user_passes_test(is_superuser_or_staff)
@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.error(request, f"Producto {producto.nombre} eliminado")
    return redirect('lista_productos')

# -------- CONFIGURACION ----------

@user_passes_test(is_superuser_or_staff)
@login_required
def configuracion(request):
    configuracion = Configuracion.objects.first() 
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST, request.FILES, instance=configuracion)
        if form.is_valid():
            form.save()  
            return redirect('configuracion')  
    else:
        form = ConfiguracionForm(instance=configuracion)
    
    return render(request, 'gestion/form_info.html', {'form': form})

# -------- CATEGORIAS ----------

@user_passes_test(is_superuser_or_staff)
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'gestion/lista_categorias.html', {'categorias': categorias})

@user_passes_test(is_superuser_or_staff)
@login_required
def buscar_categorias(request):
    query = request.GET.get('query')
    if query:
        productos = Categoria.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(marca__icontains=query)
        )
    else:
        productos = Categoria.objects.all()

    return render(request, 'gestion/lista_productos.html', {'productos': productos, 'query': query})

@user_passes_test(is_superuser_or_staff)
@login_required
def agregar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, "Categoria agregada")
            return redirect('categorias')
        else:
            print('Formulario no válido')
    else:
        form = CategoriaForm()
    return render(request, 'gestion/form_categoria.html', {'form': form})

@user_passes_test(is_superuser_or_staff)
@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.error(request, "Categoria actualizada")
            return redirect('categorias') 
        else:
            print("Formulario no válido")
            print(form.errors) 
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'gestion/form_categoria.html', {'form': form, 'categoria': categoria})

@user_passes_test(is_superuser_or_staff)
@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    messages.error(request, f"Categoria {categoria.nombre} eliminada, se eliminaron los productos asociados")
    return redirect('categorias')


# -------- USUARIOS ----------

@user_passes_test(is_superuser_or_staff)
@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    print({'usaurios': usuarios})
    return render(request, 'gestion/lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(is_superuser_or_staff)
@login_required
def buscar_usuarios(request):
    query = request.GET.get('query')
    if query:
        usuarios = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    return render(request, 'gestion/lista_usuarios.html', {'usuarios': usuarios, 'query': query})

@user_passes_test(is_superuser_or_staff)
@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario {username} creado con exito.')
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'gestion/form_usuarios.html', {'form': form})

@user_passes_test(is_superuser_or_staff)
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    # Verificar si el usuario es un superusuario
    if usuario.is_superuser:
        messages.error(request, "No se puede editar a un superusuario.")
        return redirect('usuarios')

    if request.method == 'POST':
        # Instanciar el formulario con los datos de la solicitud POST y los archivos (como imagen)
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
        else:
            print("Formulario no válido")
            print(form.errors)  # Imprimir errores para depuración
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'gestion/form_usuarios.html', {'form': form, 'usuario': usuario})

@user_passes_test(is_superuser_or_staff)
@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Verificar si el usuario es un superusuario
    if usuario.is_superuser:
        messages.error(request, "No se puede eliminar a un superusuario.")
        return redirect('usuarios')

    usuario.delete()
    messages.error(request, "Usuario eliminado.")
    return redirect('usuarios')

@user_passes_test(is_superuser_or_staff)
@login_required
def cambiar_estado_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    # Verificar si el usuario es un superusuario
    if usuario.is_superuser:
        messages.error(request, "No se puede cambiar el estado de un superusuario.")
        return redirect('usuarios')

    usuario.is_active = not usuario.is_active
    usuario.save()
    if usuario.is_active:
        messages.error(request, "Usuario activado")
    else:
        messages.error(request, "Usuario desactivado")
    return redirect('usuarios')

