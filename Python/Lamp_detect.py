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

    paths, names = image_set("pictures")
    print(paths, names)

    images = []
    for i in range(0, len(paths), 1):
        input_img = cv2.imread(paths[i])
        input_img = scale_img(input_img, 0.2)
        images.append(input_img)

    i = 0
    for image in images:
        cv2.imshow(names[i], image)
        i += 1

    cv2.waitKey(0)
