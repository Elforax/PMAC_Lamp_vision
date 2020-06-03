import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img, image_paths, image_get, img_show_all, get_contours, stack_images, pixel_count

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    thhold = [20000, 250000]
    thcanny = [5, 70]
    print(thhold)

    paths, names = image_paths("pictures/clean")
    paths2, names2 = image_paths("pictures/dirty")
    print(paths, names)
    for path in paths2:
        paths.append(path)

    images = image_get(paths)

    # processing here #
    for i in range(0, len(images), 1):
        print("New image")
        k = (7, 7)
        image = images[i]
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, k, 2.0, 2.0)
        edge = cv2.Canny(blur, thcanny[0], thcanny[1])
        erode = cv2.erode(edge, (3, 3))

        kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
        # print(kernel)

        thicc = cv2.dilate(edge, kernel)

        mask = get_contours(blur, thicc, thhold[0], thhold[1])

        pixels = pixel_count(mask)
        lamp_only = np.zeros_like(blur)
        result_image = np.zeros_like(image)
        if pixels > 50000:
            print("Lamp found")
            lamp_only = cv2.bitwise_and(blur, mask)
            mask2 = get_contours(image, lamp_only, thhold[0], thhold[1])
            result_image = cv2.bitwise_and(image, mask2)
        else:
            print("No Lamp found")

        stack = stack_images(0.5, [[image, edge], [result_image, lamp_only]])
        cv2.imshow("Image Set", stack)
        cv2.waitKey(0)
    # end proces
    #img_show_all(images, names)
