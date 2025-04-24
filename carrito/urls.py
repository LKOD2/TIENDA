from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    
    
    path('ver/', ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<int:producto_id>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),  
]
