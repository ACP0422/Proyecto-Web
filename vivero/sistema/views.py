
import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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

def registrarPlanta(request: HttpRequest)-> HttpResponse:
    if request.method == 'POST':
        
        nombre_planta = request.POST.get('nombre_planta')
        tipo_luz = request.POST.get('tipo_luz')
        tamano = request.POST.get('tamano')
        especie = request.POST.get('especie')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')  # Obtener el archivo subido

        # Validar si todos los campos están completos
        if not all([nombre_planta, tipo_luz, tamano, especie, descripcion]):
            raise ValidationError('Todos los campos son obligatorios.')

        # Convertir la imagen a base64 si existe
        imagen_base64 = None
        if imagen:
            # Leer la imagen en binario
            image_data = imagen.read()
            # Convertirla a base64
            imagen_base64 = base64.b64encode(image_data).decode('utf-8')

        planta = Planta.objects.create(
            nombre=nombre_planta,
            tipoluz=tipo_luz,
            tamano=tamano,
            especie=especie,
            descripcion=descripcion,
            imagen=imagen_base64  # Guardamos la imagen como un string base64
        )

        return redirect('catálogo') 

    return render(request, 'sistema/Vista_GestionArchivos.html')

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