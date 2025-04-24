
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def gestion_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('usuario-----------', username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('user no none--------', user)
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('gestion')
            else:
                return redirect('home')
        else:
            print('else aca esta--------', user)
            messages.error(request, 'Nombre de usuario o contraseña no validos')
    print('render login--------')
    return render(request, 'admin_auth/login.html')

def gestion_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario {username} creado con exito.')
            print('valido ---------')
            return redirect('home')
    else:
        print('no post ---------')
        form = UserRegisterForm()
    print('return ---------')
    return render(request, 'admin_auth/register.html', {'form': form})


@login_required
def gestion_logout(request):
    logout(request)
    return redirect('home')