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
    qr_code = m.ImageField()

    def __str__(self):
        return self.nombre

    def generar_qr(self):
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

        # Guardar el QR como imagen
        qr_img = qr.make_image(fill='black', back_color='white')
        qr_path = f"qr_codes/{self.nombre}_qr.png"
        full_path = os.path.join(settings.MEDIA_ROOT, qr_path)
        
        # Asegurarse de que la carpeta 'qr_codes' exista
        qr_folder = os.path.dirname(full_path)
        os.makedirs(qr_folder, exist_ok=True)
        
        # Guardar la imagen y actualizar el modelo
        qr_img.save(full_path)
        self.qr_code = qr_path
        self.save()




