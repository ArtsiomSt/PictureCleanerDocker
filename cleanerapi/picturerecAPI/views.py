import time
from copy import deepcopy
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer, PictureAPISerializer
from PIL import Image
import cv2
import numpy as np
import base64
import multiprocessing
from .functions_for_images.opencv_cleaner import clean_scaner
from .functions_for_images.autoencoder_predict import get_autoencoded_image
import pytesseract
from .models import PictureForRecognising


class RecognisePictureAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request, format=None):
        serializer = PictureAPISerializer(data=request.data)
        if serializer.is_valid():
            new_picture = serializer.save()
            path_to_img = new_picture.image.url[1:]
            img = cv2.imread(path_to_img)

            opencv_cleaning_process = multiprocessing.Process(target=clean_scaner, args=(img, new_picture), name='cleaning')
            opencv_cleaning_process.start()
            autoencoded_img = get_autoencoded_image(img)

            autoencoded_image_encode = cv2.imencode('.png', autoencoded_img)[1]
            autoencode_encode = np.array(autoencoded_image_encode)
            autoencode_byte_encode = autoencode_encode.tobytes()

            opencv_cleaning_process.join()
            new_picture = PictureForRecognising.objects.get(pk=new_picture.pk)
            cleaned_opencv_image = cv2.imread(new_picture.cleaned.url[1:])
            cleaned_opencv_image_encode = cv2.imencode('.png', cleaned_opencv_image)[1]
            cleaned_opencv_data_encode = np.array(cleaned_opencv_image_encode)
            cleaned_opencv_byte_encode = cleaned_opencv_data_encode.tobytes()
            opencv_cleaning_process.terminate()

            pil_img = Image.fromarray(autoencoded_img)
            pil_img = pil_img.convert('RGB')
            text_from_image = pytesseract.image_to_string(pil_img, lang='eng')

            new_picture.image.delete(save=False)
            new_picture.cleaned.delete(save=False)
            new_picture.delete()
            return Response({'letters': text_from_image,
                             'cleaned_img': base64.b64encode(cleaned_opencv_byte_encode),
                             'autoencoded_img': base64.b64encode(autoencode_byte_encode),
                             })
        return Response({'answer': 'Your data is not valid'})
