from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import  PictureAPISerializer
from .functions_for_images.clean_picture import  get_cleaned_picture_and_text


class RecognisePictureAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request, format=None):
        serializer = PictureAPISerializer(data=request.data)
        if serializer.is_valid():
            new_picture = serializer.save()
            path_to_img = new_picture.image.url[1:]
            autoencoded_encode, cleaned_opencv_encode, text_from_image = get_cleaned_picture_and_text(path_to_img, new_picture)
            return Response({'letters': text_from_image,
                             'cleaned_img': cleaned_opencv_encode,
                             'autoencoded_img': autoencoded_encode,
                             })
        return Response({'answer': 'Your data is not valid'})
