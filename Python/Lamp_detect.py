import numpy as np
import cv2
import os
import sys

# PMAC is een lib waar functies instaan die voor alle test scripts gebruikt kunnen worden
# import de gene die je nodig hebt
from PMAC import scale_img

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    image = cv2.imread("pictures/lamp schoon.jpg")
    image = scale_img(image, 0.2)

    cv2.imshow("Original", image)
    cv2.waitKey(0)
