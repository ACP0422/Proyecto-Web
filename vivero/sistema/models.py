from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
from django.conf import settings
from django.db import models as m

class Planta(m.Model):
    nombre = m.CharField(max_length=100)
    tipoluz = m.CharField(max_length=20)
    tamano = m.CharField(max_length=20)
    especie = m.CharField(max_length=100)
    descripcion = m.TextField()
    imagen = m.ImageField()
    qr_code = m.ImageField(upload_to='qr_codes/')  # You can specify a subdirectory for the QR codes

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

        # Guardar el QR como imagen en un objeto BytesIO
        qr_img = qr.make_image(fill='black', back_color='white')

        # Crear un archivo en memoria
        qr_image_file = BytesIO()
        qr_img.save(qr_image_file, format='PNG')
        qr_image_file.seek(0)  # Rewind the file pointer to the beginning

        # Guardar el archivo en el campo qr_code
        self.qr_code.save(f"{self.nombre}_qr.png", ContentFile(qr_image_file.read()), save=False)
        self.save()
