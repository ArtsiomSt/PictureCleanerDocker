import pytesseract
from PIL import Image
import cv2
import numpy as np
import base64
import multiprocessing

from .opencv_cleaner import clean_scaner
from .autoencoder_predict import get_autoencoded_image
from ..models import PictureForRecognising


def get_cleaned_picture_and_text(path_to_img, picture_model):
    img = cv2.imread(path_to_img)

    opencv_cleaning_process = multiprocessing.Process(target=clean_scaner, args=(img, picture_model), name='cleaning')
    opencv_cleaning_process.start()
    autoencoded_img = get_autoencoded_image(img)

    autoencoded_image_encode = cv2.imencode('.png', autoencoded_img)[1]
    autoencode_encode = np.array(autoencoded_image_encode)
    autoencode_byte_encode = autoencode_encode.tobytes()

    opencv_cleaning_process.join()
    new_picture = PictureForRecognising.objects.get(pk=picture_model.pk)
    cleaned_opencv_image = cv2.imread(new_picture.cleaned.url[1:])
    cleaned_opencv_image_encode = cv2.imencode('.png', cleaned_opencv_image)[1]
    cleaned_opencv_data_encode = np.array(cleaned_opencv_image_encode)
    cleaned_opencv_byte_encode = cleaned_opencv_data_encode.tobytes()
    opencv_cleaning_process.terminate()

    pil_img = Image.fromarray(autoencoded_img)
    pil_img = pil_img.convert('RGB')
    text_from_image = pytesseract.image_to_string(pil_img, lang='eng')
    return base64.b64encode(autoencode_byte_encode), base64.b64encode(cleaned_opencv_byte_encode), text_from_image
