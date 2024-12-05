from django.urls import path

from . import views

urlpatterns = [
    path('', views.indice, name="índice"),
    path("catalogo/", views.catalogo, name="catálogo"),
    path("sobreNosotros/", views.sobreNosotros, name="sobre_nosotros"),
    path("ficha/obtener-planta/", views.obtener_planta, name='obtener_planta'),
    path("ficha/", views.ficha, name="ficha"),
    path("registrarPlanta/", views.registrarPlanta, name="registrar_planta"),
    path("iniciarSesion/", views.iniciarSesion, name="iniciar_sesión"),
    path("cerrarSesion/", views.cerrarSesion, name="cerrar_sesión"),
    path("registrarse/", views.registrarse, name="registrarse"),
    path('catalogo/filtrarProductos/', views.filtrar_productos, name='filtrar_productos'),
]