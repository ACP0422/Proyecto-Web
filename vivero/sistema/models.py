from django.db import models as m
import qrcode
import os
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile


class Planta(m.Model):
    nombre = m.CharField(max_length=100)
    tipoluz = m.CharField(max_length=20)
    tamano = m.CharField(max_length=20)
    especie = m.CharField(max_length=100)
    descripcion = m.TextField()
    imagen = m.ImageField()
    qr_code = m.ImageField(default="qr_codes/default_qr.png")

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Generar QR solo si no existe
        if not self.qr_code:
            # Construir la URL de la ficha
            ficha_url = f"{settings.SITE_URL}/ficha?planta={self.nombre}"

            # Crear el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(ficha_url)
            qr.make(fit=True)

            # Convertir el QR en una imagen
            qr_img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_name = f"qr_{self.nombre}.png"

            # Guardar la imagen QR en el campo qr_code
            self.qr_code.save(qr_name, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

        super().save(*args, **kwargs)


