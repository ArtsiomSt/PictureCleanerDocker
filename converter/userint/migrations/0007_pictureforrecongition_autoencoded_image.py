# Generated by Django 4.1.4 on 2022-12-15 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userint', '0006_pictureforrecongition_cleaned_opencv_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictureforrecongition',
            name='autoencoded_image',
            field=models.ImageField(blank=True, null=True, upload_to='autoencoded/%Y'),
        ),
    ]