from django.db import models as m

class Planta(m.Model):
    nombre = m.CharField(max_length=100)
    tipoluz = m.CharField(max_length=20)
    tamano = m.CharField(max_length=20)
    especie = m.CharField(max_length=100)
    descripcion = m.TextField()
    imagen = m.TextField()  

    def __str__(self):
        return self.nombre


