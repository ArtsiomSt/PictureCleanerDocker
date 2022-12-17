from keras.models import load_model
import cv2
import numpy as np
from copy import deepcopy


autoencoder = load_model('autoencoder_mnist_2.h5')


def get_autoencoded_image(img):
    img_copy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = img_copy.shape
    img_copy = cv2.resize(img_copy, (512,512))
    img_copy = img_copy/255
    img_copy = np.expand_dims(img_copy, axis=0)
    img_copy = np.expand_dims(img_copy, axis=3)
    res = autoencoder.predict(img_copy)
    res = np.squeeze(res)
    res = res*255
    res = cv2.resize(res, (shape[1], shape[0]))
    return res
