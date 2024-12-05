from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError



def indice(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Indice.html")

def catalogo(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Catalogo.html")

def sobreNosotros(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_SobreNosotros.html")

def ficha(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema/Vista_Ficha.html")

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