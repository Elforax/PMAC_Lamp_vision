import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_set

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    paths, names = image_set("pictures/dirty")
    print(paths, names)

    images = []
    for i in range(0, len(paths), 1):
        input_img = cv2.imread(paths[i])
        input_img = scale_img(input_img, 0.2)
        images.append(input_img)

    rgb_image = images[1]
    hsv_image = cv2.cvtColor(images[1], cv2.COLOR_BGR2HSV)

    lowerb_c = np.array([60, 50, 50])
    upperb_c = np.array([61, 255, 255])

    mask_clean = cv2.inRange(hsv_image, lowerb_c, upperb_c)
    opp_total = cv2.countNonZero(mask_clean)
    print(opp_total)

    lamp_only_clean = cv2.bitwise_and(images[0], images[0], mask= mask_clean)
    lamp_only_dirty = cv2.bitwise_and(images[2], images[2], mask= mask_clean)
    dirt_only = cv2.bitwise_xor(lamp_only_clean, lamp_only_dirty)

    hsv_dirt = cv2.cvtColor(dirt_only, cv2.COLOR_BGR2HSV)

    cv2.imshow("hsv dirt", hsv_dirt)

    lowerb_d = np.array([1, 1, 1])
    upperb_d = np.array([180, 255, 255])

    mask_dirt = cv2.inRange(hsv_dirt, lowerb_d, lowerb_d)

    cv2.imshow("lamp only dirty", lamp_only_dirty)
    cv2.imshow("lamp only clean", lamp_only_clean)
    cv2.imshow("mask dirt", mask_dirt)

    i = 0
    for image in images:
        cv2.imshow(names[i], image)
        i += 1

    cv2.waitKey(0)
