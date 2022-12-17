import cv2
import numpy as np
import os

# this network is worse than pytesseract :(
# so it wont be used in this project :(((


def prediction(img, model):
    if 'temp_files' not in os.listdir():
        os.mkdir('temp_files')
    if not img.shape == (32, 32):
        img = cv2.resize(img, (32, 32))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)!!!!!
    #_, img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)!!!!
    cv2.imwrite('temp_files/tempimg.png', img)
    img = cv2.imread('temp_files/tempimg.png')
    img = np.expand_dims(img, axis=0)
    res = model.predict(img)
    return np.argmax(res)

