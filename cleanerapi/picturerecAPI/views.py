from copy import deepcopy
#from .functions_for_images.funcs_for_rec import get_letters_from_picture
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer, PictureAPISerializer
from .models import PictureForRecognising
from PIL import Image
import cv2
import numpy as np
import base64
from .functions_for_images.opencv_cleaner import clean_scaner
from .functions_for_images.autoencoder_predict import get_autoencoded_image
import pytesseract


#path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#pytesseract.pytesseract.tesseract_cmd = path_to_tesseract


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

            cleaned_opencv_image = clean_scaner(img)
            cleaned_opencv_image_copy = deepcopy(cleaned_opencv_image)

            autoencoded_img = get_autoencoded_image(img)
            autoencoded_image_encode = cv2.imencode('.png', autoencoded_img)[1]
            autoencode_encode = np.array(autoencoded_image_encode)
            autoencode_byte_encode = autoencode_encode.tobytes()

#            letters, rectangled_img = get_letters_from_picture(cleaned_opencv_image_copy)
#            rect_img_encode = cv2.imencode('.png', rectangled_img)[1]
#            rect_data_encode = np.array(rect_img_encode)
#            rect_byte_encode = rect_data_encode.tobytes()

            cleaned_opencv_image_encode = cv2.imencode('.png', cleaned_opencv_image)[1]
            cleaned_opencv_data_encode = np.array(cleaned_opencv_image_encode)
            cleaned_opencv_byte_encode = cleaned_opencv_data_encode.tobytes()

            pil_img = Image.fromarray(autoencoded_img)
            pil_img = pil_img.convert('RGB')
            text_from_image = pytesseract.image_to_string(pil_img, lang='eng')

            new_picture.image.delete(save=True)
            new_picture.delete()
            return Response({'letters': text_from_image,
                             #'new_img': base64.b64encode(rect_byte_encode),
                             'cleaned_img': base64.b64encode(cleaned_opencv_byte_encode),
                             'autoencoded_img': base64.b64encode(autoencode_byte_encode),
                             })
        return Response({'answer': 'success'})
