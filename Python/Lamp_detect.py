import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_paths, image_get, img_show_all, get_contours

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    paths, names = image_paths("pictures/clean")
    print(paths, names)
    images = image_get(paths)

    # processing here #
    for i in range(0, len(images), 1):
        k = (7, 7)
        image = images[i]
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, k, 2.0, 2.0)
        edge = cv2.Canny(blur, 10, 50)
        thicc = cv2.dilate(edge, (3, 3))
        mask = get_contours(image, thicc, 80000, 250000)
        lamp_only = cv2.bitwise_and(image, mask)

        erode = cv2.erode(edge, (3, 3))
        cv2.imshow("Original", image)
        cv2.imshow("blur", blur)
        cv2.imshow("edge", edge)
        cv2.imshow("mask", mask)
        cv2.imshow("lamp_only", lamp_only)
        cv2.waitKey(0)

    # end proces
    #img_show_all(images, names)
