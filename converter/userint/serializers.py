from rest_framework import serializers
from .models import PictureForRecongition


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureForRecongition
        fields = ('picture_file', 'proccesed', 'recognised_text')


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
