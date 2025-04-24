from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home-home'),
    path('categoria/<str:categoria>/', productos_por_categoria, name='productos_por_categoria'),
    path('contacto/', contacto, name='contacto'),
    path('producto/<int:producto_id>/', producto_detalle, name='producto_detalle'),
]
