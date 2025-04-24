from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('', gestion_login),
    path('login/', gestion_login, name='login'),
    path('register/', gestion_register, name='register'),
    path('logout/', gestion_logout, name='logout')
]
