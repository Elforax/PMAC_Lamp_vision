import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_paths, image_get, img_show_all, get_contours, stack_images

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    thhold = [80000, 250000]
    print(thhold)

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
        mask = get_contours(image, thicc, thhold[0], thhold[1])

        lamp_only = cv2.bitwise_and(image, mask)

        stack = stack_images(0.5, [[image, edge], [mask, lamp_only]])
        cv2.imshow("Image Set", stack)
        cv2.waitKey(0)
    # end proces
    #img_show_all(images, names)
