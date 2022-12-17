from copy import deepcopy
import cv2
from .neiro_predict import prediction
from keras.models import load_model
from .rename_fnt import res, res_dir
import os

model = load_model('letter_rec_new_v5.h5')

dangerous_letters = ['C', 'c', 'I', 'i', 'O', 'o', 'S', 's', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Z', 'z']


def get_picc(impath):  # outdated function
    out_size = 32
    image_file = f"{impath}"
    img = cv2.imread(image_file)
    img_copy = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = sorted(contours, key=cv2.contourArea, reverse=True)
    letters = []
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hierarchy[0][idx][3] == 0:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            letter_crop = img_copy[y:y + h, x:x + w]
            print(cv2.contourArea(item))
            letters.append((x, y, cv2.resize(letter_crop, (out_size, out_size))))
    letters.sort(key=lambda x: x[0])
    cv2.imshow('img', img)
    cv2.waitKey(0)
    return letters


#    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 3)

def get_letters_from_picture(img):
    out_size = 32
    img_copy = deepcopy(img)
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)
    thresh = img # !!!!!!!!!!!!!!!!HERE IS THE CHANGE(FOR ME NOT TO LOSE THIS MOMENT)
    conts, hier = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    biggest = 0
    letters = []
    for idx, item in enumerate(conts):
        if cv2.contourArea(item) > 0.8 * img.shape[0] * img.shape[1]:
            biggest = idx
    areas = list(map(cv2.contourArea, sorted(conts, key=cv2.contourArea)[1:]))
    avg_area = sum(areas) / (10 * len(areas))
    current_height = None
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hier[0][idx][3] == biggest and cv2.contourArea(item) > avg_area:
            if current_height is None:
                current_height = y + h
                line = 0
            letter_height = y + h
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            letter_crop = img_copy[y:y + h, x:x + w]
            if not (letter_height < float(current_height) + h / 3 and letter_height > float(current_height) - h):
                current_height = y + h
                line += 1
            letters.append((x, w, cv2.resize(letter_crop, (out_size, out_size)), line, h))
    new_letters = sort_letters_by(letters)
    return new_letters, img


def array_of_letters_to_str(letters):
    predicted = []
    list_of_letters = []
    x_prev = w_prev = None
    avg_width = sum(map(lambda x: x[1], filter(lambda x: len(x) == 5, letters))) / len(letters)
    avg_height = sum(map(lambda x: x[4], filter(lambda x: len(x) == 5, letters))) / len(letters)
    for i, letter in enumerate(letters):
        if all((x_prev, w_prev)) and letter[0] - (x_prev + w_prev) > avg_width / 4:
            list_of_letters.append(' ')
        if letter[2] == "\n":
            list_of_letters.append("\n")
            continue
        pred = prediction(letter[2], model)
        predicted.append(pred)
        current_letter = res_dir[pred + 10]
        if current_letter in dangerous_letters:
            if letter[4] > avg_height:
                if not (ord(current_letter) > ord('A') - 1 and ord(current_letter) < ord('Z') + 1):
                    current_letter = res_dir[pred+10-26]
            else:
                if not (ord(current_letter) > ord('a') - 1 and ord(current_letter) < ord('z') + 1):
                    current_letter = res_dir[pred+10+26]
        #list_of_letters.append(res_dir[pred + 10])
        list_of_letters.append(current_letter)
        x_prev, w_prev = letter[0], letter[1]
    return list_of_letters


def sort_letters_by(letters):
    max_line_element = max(letters, key=lambda x: x[3])
    max_line = max_line_element[3] + 1
    line = 0
    new_letters = []
    while (line < max_line):
        part_of_letters = list(filter(lambda x: x[3] == line, letters))
        part_of_letters.sort(key=lambda x: x[0])
        part_of_letters.append((1, 1, "\n", 1))
        new_letters = part_of_letters + new_letters
        line += 1
    return new_letters


def picture_to_one_letter(picture):
    letter = prediction(picture, model)
    print(letter)
    return res_dir[letter]


def letters_to_file(letters):
    counter = 0
    for img in letters:
        cv2.imwrite(f'temp/{counter}.png', img[2])
        counter += 1
    return


def get_text_from_picture(img):  # function that will give text direcly from image, without other info
    pass
