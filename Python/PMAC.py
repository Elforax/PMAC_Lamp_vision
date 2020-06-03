import numpy as np
import cv2
import os
import sys
import glob

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt


def scale_img(img, scale=1.0):
    _scale_v = round(len(img) * scale)
    _scale_u = round(len(img[0]) * scale)

    print(_scale_u, "x", _scale_v)
    _img = cv2.resize(img, (_scale_u, _scale_v))
    return _img


def get_contours(img, edge, rangeMin, rangeMax):
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in range(0, len(contours), 1):
        color_set = (0, 0, 255)
        area = cv2.contourArea(contours[i])
        print(area)
        mask = np.zeros_like(img)
        if rangeMin < area < rangeMax:
            cv2.fillPoly(mask, pts=[contours[i]], color=(255, 255, 255))

            offset = 10
            x, y, w, h = cv2.boundingRect(contours[i])
            img = cv2.rectangle(img, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 2)
            return mask


def image_paths(path, file_type="jpg"):    # points to a folder and takes all the images in it.
    _data = glob.glob(path + "/*." + file_type)

    _paths = []
    _names = []
    for file in _data:
        _split_data = file.split("\\")

        _file_path = path + "/" + _split_data[len(_split_data)-1]

        _names.append(_split_data[len(_split_data)-1])
        _paths.append(_file_path)
    return _paths, _names


def image_get(paths):
    _images = []
    for i in range(0, len(paths), 1):
        _input_img = cv2.imread(paths[i])
        _input_img = scale_img(_input_img, 0.2)
        _images.append(_input_img)
    return _images

def img_show_all(img, names):
    i = 0
    for image in img:
        cv2.imshow(names[i], image)
        i += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()