from django.db import models as m

class Planta(m.Model):
    nombre = m.CharField(max_length=50)
    tipoluz = m.CharField(max_length=50)
    tamano = m.CharField(max_length=50)
    especie = m.CharField(max_length=50)
    descripcion = m.TextField()
    imagen = m.ImageField()

    def __str__(self):
        return self.nombre


