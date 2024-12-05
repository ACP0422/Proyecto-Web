from django.urls import path

from . import views

urlpatterns = [
    path('', views.indice, name="índice"),
    path("catalogo/", views.catalogo, name="catálogo"),
    path("sobreNosotros/", views.sobreNosotros, name="sobre_nosotros"),
    path("ficha/", views.ficha, name="ficha"),
    path("registrar_planta/", views.registrarPlanta, name="registrar_planta")
]