import os
import sys
import numpy as np
import cv2
from Python.Lamp_detect import find_lamp
from Python.PMAC import *
print(__name__)
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets dir to current dir

    paths, names = image_paths("pictures/dirty")  # gets all image paths and names
    paths2, names2 = image_paths("pictures/dirty_alt")
    for path in paths2:
        paths.append(path)  # appends one list to the other

    for name in names2:
        names.append(name)  # appends one list to the other
    print(paths)

    # processing here #
    results = []
    index = 0
    for path in paths:
        image = cv2.imread(path)
        image = scale_img(image, 0.2)
        print("New lamp")
        result, area, _process = find_lamp(image)
        if area == 0:
            continue
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        kernel_star = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)      # creates a star kernel
        kernel_box = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)  # creates a star kernel

        mask = cv2.inRange(gray, 1, 255)
        mask = cv2.erode(mask, kernel_star, iterations=3)

        blur = cv2.GaussianBlur(gray, (15, 15), 3.0, 3.0)
        edge = cv2.Canny(blur, 50, 150)
        define_edge = cv2.dilate(edge, kernel_star)

        # LED border boc compensation (Removes te gray border around the LEDs)
        mask_led_border = cv2.inRange(hsv, (10, 60, 50), (20, 80, 100))
        mask_led_border = cv2.dilate(mask_led_border, kernel_star, iterations=2)
        mask_led_border = cv2.erode(mask_led_border, kernel_box, iterations=2)
        mask_led_border = cv2.dilate(mask_led_border, kernel_star, iterations=4)
        inv_mask_leds = cv2.bitwise_not(mask_led_border)
        inv_mask_leds = cv2.bitwise_and(inv_mask_leds, mask)

        # hsv color mask    (Finds difference in colors compared to the lamp)
        mask_hsv = cv2.inRange(hsv, (5, 20, 100), (40, 80, 255))
        inv_mask_hsv = cv2.bitwise_not(mask_hsv)
        inv_mask_hsv = cv2.bitwise_and(inv_mask_hsv, mask)
        inv_mask_hsv = cv2.erode(inv_mask_hsv, kernel_star, iterations=1)

        # mean image mask   (Finds deltas from the mean of the grayscale)
        mean = np.mean(gray)
        mean_map = np.ones_like(gray)
        mean_map[:] = mean

        invert = gray - mean_map
        invert_edge = cv2.Canny(invert, 100, 100)
        invert_edge_dilate = cv2.dilate(invert_edge, kernel_star, iterations=2)
        invert_edge_dilate = cv2.bitwise_and(invert_edge_dilate, mask)
        invert_edge_dilate = cv2.erode(invert_edge_dilate, kernel_star, iterations=1)

        # noise amplified mask (Finds quick changes in the surface texture of te image)
        blur_invert = cv2.GaussianBlur(invert, (11, 11), 2.0, 2.0)
        noise = invert - blur_invert
        erode = cv2.erode(noise, kernel_star, iterations=2)
        dilate = cv2.dilate(erode, kernel_star, iterations=5)
        noise_mask = cv2.inRange(invert_edge_dilate, 10, 255)
        noise_mask = cv2.bitwise_and(noise_mask, mask)
        noise_mask = cv2.erode(noise_mask, kernel_star, iterations=1)


        noise_compliment = cv2.bitwise_and(noise_mask, invert_edge_dilate)
        dirty_zone = cv2.bitwise_or(noise_compliment, inv_mask_hsv)
        dirty_zone = cv2.bitwise_and(dirty_zone, inv_mask_leds)

        dirtiness_results = cv2.copyTo(result, np.ones_like(result))
        dirtiness_results[dirty_zone > 0] = (255, 0, 0)


        dirty_pixels = pixel_count(dirty_zone)
        lamp_area = pixel_count(mask)
        dirtiness = round((dirty_pixels/lamp_area) * 100.0, 2)
        if dirtiness < 0:
            dirtiness = 0

        print(area, dirty_pixels)
        print(str(names[index]),": ",dirtiness, "%")
        stack = stack_images(0.4, [[result, gray, hsv], [dirtiness_results, dirty_zone, inv_mask_hsv], [noise, invert, mask_led_border],[noise_mask, invert_edge_dilate, inv_mask_leds]])
        cv2.imshow("Results", stack)

        cv2.waitKey(0)
        index += 1
    cv2.destroyAllWindows()
