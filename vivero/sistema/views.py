from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


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