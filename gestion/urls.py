from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion_home, name='gestion'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/buscar/', views.buscar_productos, name='buscar_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    

    path('configuracion/', views.configuracion, name='configuracion'),
    
    # ---- CATEGORIAS ----
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/buscar/', views.buscar_categorias, name='buscar_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # ---- USUARIOS ----
    path('usuarios/', views.lista_usuarios, name='usuarios'),
    path('usuarios/buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuarios'),
    path('usuarios/cambiar-estado/<int:usuario_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),


]
