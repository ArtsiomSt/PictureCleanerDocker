# Generated by Django 4.1.3 on 2022-12-02 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userint', '0003_delete_pictureforrecongition'),
    ]

    operations = [
        migrations.CreateModel(
            name='PictureForRecongition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture_file', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('recognised_text', models.TextField(blank=True, default='', null=True)),
                ('proccesed', models.BooleanField(default=False)),
                ('made_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userint.userprofile')),
            ],
        ),
    ]