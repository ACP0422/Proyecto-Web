
import base64
#import imghdr
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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

def obtener_planta(request):
    print("Obteniendo planta con ID:", request.GET.get('planta'))
    plantas = Planta.objects.all()
    for planta in plantas:
        print(planta.nombre, planta.especie)  # Ajusta los campos que quieres ver


    planta_id = request.GET.get('planta')
    try:
        planta = Planta.objects.get(nombre=planta_id)
        data = {
            "nombre": planta.nombre,
            "nombreCientifico": planta.especie,
            "descripcion": planta.descripcion,
            "detalles": {
                "familia": planta.especie,  
                "luz": planta.tipoluz,         
                "tamano": planta.tamano,  
                "riego": "Riego pendiente",    
                "clima": "Clima pendiente",     
                "uso": "Uso pendiente",        
                "cuidados": "Cuidados pendientes" 
            },
            "imagenPrincipal": planta.imagen.url if planta.imagen else "",
            "imagenesRelacionadas": [],  # Agrega lógica si tienes más imágenes relacionadas
            "qr": planta.qr_code.url if planta.qr_code else ""
        }
        return JsonResponse(data)
    except Planta.DoesNotExist:
        return JsonResponse({"error": "Planta no encontrada"}, status=404)


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

        # Validar tipo de archivo
        tipo_imagen = imghdr.what(imagen)
        if tipo_imagen not in ['jpeg', 'png', 'gif']:
            raise ValidationError('Solo se permiten imágenes JPEG, PNG o GIF.')

        # Codificar la imagen en Base64
        imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        planta = Planta.objects.create(
            nombre=nombre_planta,
            tipoluz=tipo_luz,
            tamano=tamano,
            especie=especie,
            descripcion=descripcion,
            imagen=imagen_base64  # Guardamos la imagen como un string base64
        )
        planta.generar_qr()

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
    

def filtrar_productos(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        tipos_de_luz = data.get("tipo_de_luz", [])
        tamaños = data.get("tamaño", [])
        especies = data.get("especie", [])

        print(data.get("tipo_de_luz", []))
        print(data.get("tamaño", []))
        print(data.get("especie", []))

        # Filtrar productos según los criterios
        productos = Planta.objects.all()
        if tipos_de_luz:
            # Filtrar usando __iexact para hacer comparaciones insensibles a mayúsculas
            condiciones_luz = [Q(tipoluz__iexact=tipo) for tipo in tipos_de_luz]
            productos = productos.filter(*condiciones_luz)
        if tamaños:
            # Filtrar usando __iexact
            condiciones_tamaño = [Q(tamano__iexact=tamaño) for tamaño in tamaños]
            productos = productos.filter(*condiciones_tamaño)
        if especies:
            # Filtrar usando __iexact
            condiciones_especie = [Q(especie__iexact=especie) for especie in especies]
            productos = productos.filter(*condiciones_especie)

        # Verificar los valores filtrados
        print("Productos filtrados:", productos)

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


