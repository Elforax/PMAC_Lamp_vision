import numpy as np
import cv2
import os
import sys

print("You are using OpenCV version " + cv2.__version__ + ".")

if __name__ == "__main__":
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Path = "pictures/"
    images = ["lamp schoon.jpg", "lamp schoon alt.jpg", "lamp schoon alt 2.jpg"]

    dataset_path = []
    for image in images:
        dataset_path.append(Path+image)

    dataset = []
    for data in dataset_path:
        dataset.append(cv2.imread(data))

    print(len(dataset))
    for i in range(0, len(dataset), 1):
        print(dataset[i])

        pass

