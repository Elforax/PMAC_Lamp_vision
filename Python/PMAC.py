import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt


def scale_img(img, scale=1.0):
    scale_v = round(len(img) * scale)
    scale_u = round(len(img[0]) * scale)

    print(scale_u, "x" ,scale_v)
    img = cv2.resize(img, (scale_u, scale_v))
    return img
