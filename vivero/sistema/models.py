from django.db import models as m
import qrcode
import os
from django.conf import settings

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
    
    def generate_qr_img(self):

        url_qr = f"{settings.SITE_URL}/ficha?planta={self.nombre}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url_qr)
        qr.make(fit=True)

        qr_img = qr.make_image(fill='black', back_color='white')
        qr_path = f"qr_codes/{self.nombre}_qr.png"
        full_path = os.path.join(settings.MEDIA_ROOT, qr_path)
        qr_img.save(full_path)
        self.qr_code = qr_path
        self.save()


