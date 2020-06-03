import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_paths

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    paths_ref, names_ref = image_paths("pictures/ref")
    print(paths_ref, names_ref)
    paths, names = image_paths("pictures/dirty")
    print(paths, names)

#refrance data
    images_ref = []
    for i in range(0, len(paths_ref), 1):
        input_img_ref = cv2.imread(paths_ref[i])
        input_img_ref = scale_img(input_img_ref, 0.2)
        images_ref.append(input_img_ref)

    hsv_image = cv2.cvtColor(images_ref[1], cv2.COLOR_BGR2HSV)

    lowerb_c = np.array([60, 50, 50])
    upperb_c = np.array([61, 255, 255])
    mask_clean = cv2.inRange(hsv_image, lowerb_c, upperb_c)
    opp_total = cv2.countNonZero(mask_clean)

    lamp_only_clean = cv2.bitwise_and(images_ref[0], images_ref[0], mask= mask_clean)

#dirt data
    images = []
    for i in range(0, len(paths), 1):
        input_img = cv2.imread(paths[i])
        input_img = scale_img(input_img, 0.2)
        images.append(input_img)

        lamp_only_dirty = cv2.bitwise_and(images[i], images[i], mask= mask_clean)
        dirt_only = cv2.bitwise_xor(lamp_only_clean, lamp_only_dirty)

        hsv_dirt = cv2.cvtColor(dirt_only, cv2.COLOR_BGR2HSV)

        lowerb_d = np.array([0, 0, 0])
        upperb_d = np.array([180, 255, 255])
        mask_dirt = cv2.inRange(hsv_dirt, lowerb_d, lowerb_d)
        mask_dirt = cv2.bitwise_not(mask_dirt)
        opp_dirt = cv2.countNonZero(mask_dirt)

        print(names[i], opp_dirt/opp_total*100)

    if 0:
        print(opp_dirt)
        print(opp_total)
        cv2.imshow("mask clean", mask_clean)
        cv2.imshow("hsv dirt", hsv_dirt)
        cv2.imshow("mask dirt", mask_dirt)
        cv2.imshow("lamp only dirty", lamp_only_dirty)
        cv2.imshow("lamp only clean", lamp_only_clean)

        i = 0
        for image in images:
            cv2.imshow(names[i], image)
            i += 1

    cv2.waitKey(0)
