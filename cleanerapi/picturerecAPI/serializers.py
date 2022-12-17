from rest_framework import serializers
from .models import PictureForRecognising


class PictureAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureForRecognising
        fields = '__all__'


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
