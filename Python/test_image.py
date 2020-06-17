import numpy as np
import cv2
import os
from Python.Lamp_detect import find_lamp

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_paths

print("You are using OpenCV version " + cv2.__version__ + ".")
scale = .2

#debug config
debug_clean = 0
debug_dirty = 0
debug_clean_alt = 0
debug_dirty_alt = 0

#run debug
clean = 1
dirty = 0
clean_alt = 1
dirty_alt = 0

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    paths_ref, names_ref = image_paths("pictures/ref", "PNG")
    print(paths_ref, names_ref)
    paths, names = image_paths("pictures/dirty", "PNG")
    print(paths, names)
    paths_ref_alt, names_ref_alt = image_paths("pictures/ref_alt", "PNG")
    print(paths_ref_alt, names_ref_alt)
    paths_alt, names_alt = image_paths("pictures/dirty_alt", "PNG")
    print(paths_alt, names_alt)

#refrance data
    if clean:
        images_ref = []
        for i in range(0, len(paths_ref), 1):
            input_img_ref = cv2.imread(paths_ref[i])
            input_img_ref = scale_img(input_img_ref, scale)
            images_ref.append(input_img_ref)

        hsv_image = cv2.cvtColor(images_ref[1], cv2.COLOR_BGR2HSV)

        lowerb_c = np.array([60, 50, 50])
        upperb_c = np.array([61, 255, 255])
        mask_clean = cv2.inRange(hsv_image, lowerb_c, upperb_c)
        opp_total = cv2.countNonZero(mask_clean)

        lamp_only_clean = cv2.bitwise_and(images_ref[0], images_ref[0], mask= mask_clean)
        print("Lamp schoon.jpg", 0.00)

        if debug_clean:
            print(opp_total)
            cv2.imshow("lamp clean colort", images_ref[1])
            cv2.imshow("lamp clean", images_ref[0])
            cv2.imshow("mask clean", mask_clean)
            cv2.imshow("lamp only clean", lamp_only_clean)

#refrance data alt

    if clean_alt:
        images_ref_alt = []
        for i in range(0, len(paths_ref), 1):
            input_img_ref_alt = cv2.imread(paths_ref_alt[i])
            input_img_ref_alt = scale_img(input_img_ref_alt, scale)
            images_ref_alt.append(input_img_ref_alt)

        hsv_image_alt = cv2.cvtColor(images_ref_alt[0], cv2.COLOR_BGR2HSV)

        lowerb_c_alt = np.array([60, 50, 50])
        upperb_c_alt = np.array([61, 255, 255])
        mask_clean_alt = cv2.inRange(hsv_image_alt, lowerb_c_alt, upperb_c_alt)
        opp_total_alt = cv2.countNonZero(mask_clean_alt)

        lamp_only_clean_alt = cv2.bitwise_and(images_ref_alt[1], images_ref_alt[1], mask= mask_clean_alt)

        print("Lamp schoon alt.jpg", 0.00)

        if debug_clean_alt:
            print(opp_total_alt)
            cv2.imshow("lamp clean", input_img_ref_alt)
            cv2.imshow("mask clean_alt", mask_clean_alt)
            cv2.imshow("lamp only clean_alt", lamp_only_clean_alt)

#dirt data
    print("pictures")
    if dirty:
        images = []
        for i in range(0, len(paths), 1):
            input_img = cv2.imread(paths[i])
            input_img = scale_img(input_img, scale)
            images.append(input_img)

            lamp_only_dirty = cv2.bitwise_and(images[i], images[i], mask= mask_clean)
            dirt_only = cv2.bitwise_xor(lamp_only_clean, lamp_only_dirty)

            hsv_dirt = cv2.cvtColor(dirt_only, cv2.COLOR_BGR2HSV)

            lowerb_d = np.array([0, 0, 0])
            upperb_d = np.array([180, 255, 255])
            mask_dirt = cv2.inRange(hsv_dirt, lowerb_d, lowerb_d)
            mask_dirt = cv2.bitwise_not(mask_dirt)
            opp_dirt = cv2.countNonZero(mask_dirt)
            _, area, _ = find_lamp(images[i])
            if area == 0:
                area = 1
            percentage = opp_dirt / opp_total * 100
            percentage_comp = (opp_total / area) * percentage

            print(names[i], percentage_comp)

            if debug_dirty:
                print("opp_dirt", opp_dirt)
                print("opp_total", opp_total)
                cv2.imshow("dirty image", images[i])
                cv2.imshow("dirty image", images[i])
                cv2.imshow("dirt only", dirt_only)
                cv2.imshow("hsv dirt", hsv_dirt)
                cv2.imshow("lamp only dirty", lamp_only_dirty)
                cv2.imshow("mask dirt", mask_dirt)
                cv2.waitKey(0)


#dirty data alt
    print("pictures alt")
    if dirty_alt:
        images_alt = []
        for i in range(0, len(paths_alt), 1):
            input_img_alt = cv2.imread(paths_alt[i])
            input_img_alt = scale_img(input_img_alt, scale)
            images_alt.append(input_img_alt)

            lamp_only_dirty_alt = cv2.bitwise_and(images_alt[i], images_alt[i], mask=mask_clean_alt)
            dirt_only_alt = cv2.bitwise_xor(lamp_only_clean_alt, lamp_only_dirty_alt)

            hsv_dirt_alt = cv2.cvtColor(dirt_only_alt, cv2.COLOR_BGR2HSV)

            lowerb_d_alt = np.array([0, 0, 0])
            upperb_d_alt = np.array([180, 255, 255])
            mask_dirt_alt = cv2.inRange(hsv_dirt_alt, lowerb_d_alt, lowerb_d_alt)
            mask_dirt_alt = cv2.bitwise_not(mask_dirt_alt)
            opp_dirt_alt = cv2.countNonZero(mask_dirt_alt)
            _, area, _ = find_lamp(images_alt[i])
            if area == 0:
                area = 1

            percentage = opp_dirt_alt / opp_total_alt * 100
            percentage_comp = (opp_total_alt / area) * percentage

            print(names_alt[i], percentage_comp)

            if debug_dirty_alt:
                print("opp_dirt_alt", opp_dirt_alt)
                print("opp_total_alt", opp_total_alt)
                cv2.imshow("dirt only", dirt_only_alt)
                cv2.imshow("hsv dirt", hsv_dirt_alt)
                cv2.imshow("Lamp only clean", lamp_only_clean_alt)
                cv2.imshow("lamp only dirty", lamp_only_dirty_alt)
                cv2.imshow("mask dirt", mask_dirt_alt)
                cv2.waitKey(0)

cv2.waitKey(0)
