from django.shortcuts import render

# Create your views here.

def ver_resumen(request):
    return render(request, 'ventas_page/resumen.html')

def ver_ventas(request):
    return render(request, 'ventas_page/ventas.html')


