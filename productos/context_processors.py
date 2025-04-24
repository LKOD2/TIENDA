# context_processors.py
from .models import Configuracion

def configuracion_context(request):
    configuracion = Configuracion.objects.first()
    return {'configuracion': configuracion}
