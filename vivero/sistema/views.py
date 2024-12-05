from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Planta



def indice(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Indice.html")

def catalogo(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Catalogo.html")

def sobreNosotros(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_SobreNosotros.html")

def ficha(request: HttpRequest) -> HttpResponse:
    planta = request.GET.get('planta', None) 
    return render(request, "sistema/Vista_Ficha.html", {'planta': planta})

def registrarPlanta(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_GestionArchivos.html")


def indice(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Indice.html")

def iniciarSesion(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":

        # Intentar iniciar sesión
        nombreUsuario = request.POST["nombre_usuario"]
        contrasena = request.POST["contrasena"]
        usuario = authenticate(request, username=nombreUsuario, password=contrasena)

        # Validar usuario existente
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect(reverse("índice"))
        else:
            return render(request, "sistema/Vista_IniciarSesion.html", {
                "mensaje": "Nombre de usuario o contraseña incorrectos."
            })
    else:
        return render(request, "sistema/Vista_IniciarSesion.html")
    
def cerrarSesion(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("índice"))

def registrarse(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        nombreUsuario = request.POST["nombre_usuario"]
        email = request.POST["email"]

        # Comparando contraseña confirmada
        contrasena = request.POST["contrasena"]   
        confirmacion = request.POST["confirmacion"]
        if contrasena != confirmacion:
            return render(request, "sistema/Vista_Registrarse.html", {
                "mensaje": "Las contraseñas no son iguales."
            })

        # Intentar crear usuario nuevo
        try:
            usuario = User.objects.create_user(nombreUsuario, email, contrasena)
            usuario.save()
        except IntegrityError:
            return render(request, "sistema/Vista_Registrarse.html", {
                "mensaje": "Nombre de usuario ocupado."
            })
        login(request, usuario)
        return HttpResponseRedirect(reverse("índice"))
    else:
        return render(request, "sistema/Vista_Registrarse.html")
    

@csrf_exempt  # Esto es para pruebas, asegúrate de manejar CSRF correctamente en producción
def filtrar_productos(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tipo_de_luz = data.get("tipo_de_luz", [])
        tamaño = data.get("tamaño", [])
        especie = data.get("especie", [])

        # Filtrar productos según los criterios
        productos = Planta.objects.all()
        if tipo_de_luz:
            productos = productos.filter(tipoluz=tipo_de_luz)
        if tamaño:
            productos = productos.filter(tamano=tamaño)
        if especie:
            productos = productos.filter(especie=especie)

        # Serializar los datos
        productos_data = [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "imagen": producto.imagen.url
            }
            for producto in productos
        ]
        return JsonResponse({"productos": productos_data}, safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

