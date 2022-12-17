from copy import deepcopy
import cv2
import numpy as np


def clean_scaner(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 23)
    new_gray = cv2.blur(gray, (2, 2))
    thresh_mask = cv2.adaptiveThreshold(new_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 15)
    make_small_contours_white(thresh_mask)
    thresh_mask = cv2.blur(thresh, (2, 2))
    thresh = cv2.bitwise_and(thresh, thresh, mask=thresh_mask)
    make_small_contours_white(thresh)
    thresh = cv2.blur(thresh, (2, 2))
    return thresh


def make_small_contours_white(img):
    conts, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # img = cv2.drawContours(img, conts, -1, (0,255,0), 1)
    for idx, item in enumerate(conts):
        if cv2.contourArea(item) > 0.8 * img.shape[0] * img.shape[1]:
            biggest = idx
    areas = list(map(cv2.contourArea, sorted(conts, key=cv2.contourArea)[1:]))
    avg_area = sum(areas) / (50 * len(areas))
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hier[0][idx][3] == biggest and (cv2.contourArea(item) < avg_area or h < 3 or w < 3):
            img[y:y + h, x:x + w] = 255
    return img



