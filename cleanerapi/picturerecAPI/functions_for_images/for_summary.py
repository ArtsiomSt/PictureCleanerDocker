import cv2
from autoencoder_predict import get_autoencoded_image
import os
from opencv_cleaner import clean_scaner


base_dir = 'C:\\Users\\arteo\\Desktop\\Samples\\op\\'

for file in os.listdir(base_dir):
    cur_file = os.path.join(base_dir, file)
    img = cv2.imread(cur_file)
    autoencoded = get_autoencoded_image(img)
    opencved = clean_scaner(img)
    cv2.imshow('Original', img)
    cv2.imshow('Autoencoder', autoencoded/255)
    cv2.imshow('OpenCV', opencved)
    cv2.waitKey(0)
