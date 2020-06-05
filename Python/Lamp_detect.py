import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from Python.PMAC import *
print("You are using OpenCV version " + cv2.__version__ + ".")


# looks for a lamp in the image and returns a cut version of the origional image if found else the return is blank
def find_lamp(image, thhold=None, thcanny=None, k=(9, 9), stk_scale=0.5):
    if thcanny is None:
        thcanny = [5, 70]
    if thhold is None:
        thhold = [20000, 250000]

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                      # makes a grayscale version of the input
    blur = cv2.GaussianBlur(grey, k, 2.0, 2.0)                          # blurs the grayscale to reduce noise
    cv2.imshow("blur", blur)
    edge = cv2.Canny(blur, thcanny[0], thcanny[1],)                      # detects edges of the blurred image

    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)      # creates a star kernel

    thicc = cv2.dilate(edge, kernel)                                    # dilates the edges

    cv2.imshow("Mask thicc", thicc)
    mask = get_contours(blur, thicc, thhold[0], thhold[1])              # creates a mask of the filled contour

    # creates blank images to fill
    pixels = pixel_count(mask)
    _lamp = np.zeros_like(blur)
    _result_image = np.zeros_like(image)
    mask2 = np.zeros_like(image)
    _area = 0

    # if lamp is found preform this
    if pixels > 70000:
        _lamp = cv2.bitwise_and(blur, mask)                         # mask blur image for second check
        mask2 = get_contours(image, _lamp, thhold[0], thhold[1])    # second contour check to find the real lamp
        _result_image = cv2.bitwise_and(image, mask2)               # mask the result over the input image
        if _result_image.any():
            _area = pixel_count(_result_image)

    _stack = stack_images(stk_scale, [[image, edge], [_lamp, mask2]])   # create a image of multiple images

    return _result_image, _area, _stack


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))            # sets dir to current dir

    paths, names = image_paths("pictures/clean")                    # gets all image paths and names
    paths2, names2 = image_paths("pictures/dirty")
    for path in paths2:
        paths.append(path)                                           # appends one list to the other

    print(paths)

    images = image_get(paths)

    # processing here #
    results = []
    for i in range(0, len(images), 1):
        print("New image")

        result, area, stack = find_lamp(images[i])
        print(area)
        if area > 0:
            print("Found a lamp")
        else:
            print("Found a no lamp")
    # end proces

        results = [result, stack]
        img_show_all(results, ["Result", "Process Results"], False)
    cv2.destroyAllWindows()