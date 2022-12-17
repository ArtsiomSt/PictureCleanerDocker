from django.db import models

# Create your models here.


class PictureForRecognising(models.Model):
    image = models.ImageField(upload_to='recgnising/%Y/%m/')
    recognised_text = models.TextField(blank=True, null=True, default='')
    proccesed = models.BooleanField(default=False)
