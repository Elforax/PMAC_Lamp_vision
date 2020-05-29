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


def image_set(path, file_type="jpg"):    # points to a folder and takes all the images in it.
    _data = glob.glob(path + "/*." + file_type)

    _paths = []
    _names = []
    for file in _data:
        _split_data = file.split("\\")

        _file_path = path + "/" + _split_data[len(_split_data)-1]

        _names.append(_split_data[len(_split_data)-1])
        _paths.append(_file_path)
    return _paths, _names
