
from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('resumen/', ver_resumen, name='ver_resumen')
]