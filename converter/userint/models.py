from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
import os
from fpdf import FPDF
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount_of_operations = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)


class PictureForRecongition(models.Model):
    made_by_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    picture_file = models.ImageField(upload_to='photos/%Y/%m/%d')
    recognised_text = models.TextField(blank=True, null=True, default='')
    proccesed = models.BooleanField(default=False)
    rectangled_image = models.ImageField(upload_to='rectangled/%Y/%m/%d', null=True, blank=True, max_length=300)
    cleaned_opencv_image = models.ImageField(upload_to='cleaned/%Y/%m/%d', null=True, blank=True)
    autoencoded_image = models.ImageField(upload_to='autoencoded/%Y', null=True, blank=True)


    def create_pdf(self, opencv_version=False):
        if not self.proccesed:
            return
        if not 'tempfiles' in os.listdir():
            os.mkdir('tempfiles')
        current_path = 'tempfiles'
        if opencv_version:
            picture_for_pdf_file = Image.open(self.cleaned_opencv_image.url[1:])
        else:
            picture_for_pdf_file = Image.open(self.autoencoded_image.url[1:])
        text_lines = self.recognised_text.split(sep='\n')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', 'B', size=14)
        pdf.oversized_images = "DOWNSCALE"
        height_for_image = 10
        for line in text_lines:
            pdf.cell(200, 10, line, align='L')
            pdf.ln(7)
            height_for_image += 10
        if height_for_image > 2*pdf.eph/3:
            x_cord_image = 0
            pdf.add_page()
            y_cord_image = 10
        else:
            x_cord_image = 0
            y_cord_image = height_for_image
        pdf.image(picture_for_pdf_file, x=x_cord_image, y=y_cord_image)
        filename = f'pdf_{self.pk}_co.pdf' if opencv_version else f'pdf_{self.pk}_ca.pdf'
        pdf.output(os.path.join(current_path, filename))
        return os.path.join(current_path, filename)
