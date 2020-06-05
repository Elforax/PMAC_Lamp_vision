import os
import sys
import numpy as np
import cv2
from Python.Lamp_detect import find_lamp
from Python.PMAC import *
print(__name__)
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets dir to current dir

    paths, names = image_paths("pictures/clean")  # gets all image paths and names
    paths2, names2 = image_paths("pictures/dirty")
    for path in paths2:
        paths.append(path)  # appends one list to the other

    print(paths)
