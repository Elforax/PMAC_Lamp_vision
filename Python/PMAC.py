import numpy as np      # numpy
import cv2              # opencv
import glob             # file and directory controller

# PMAC is a lib that contains all functions shared by the other scripts
# import the ones you need


def scale_img(img, scale=1.0):                      # scales a given image with the scale (default=1.0)
    _scale_v = round(len(img) * scale)              # gets a rounded value for the height of the image
    _scale_u = round(len(img[0]) * scale)           # gets a rounded value for the width of the image

    _img = cv2.resize(img, (_scale_u, _scale_v))    # resizes the image to the correct size
    return _img


def get_contours(img, edge, rangeMin, rangeMax):    # find the contours of and object in an image
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros_like(img)                       # make a empty mask the size of the input image

    biggest = []
    for i in range(0, len(contours), 1):            # loop through all contours
        area = cv2.contourArea(contours[i])
        # cv2.drawContours(img, contours[i], -1, (0, 0, 255), 2)

        max_area = 0
        if rangeMin < area < rangeMax:                  # only uses the contours withing the threshold area
            cv2.fillPoly(mask, pts=[contours[i]], color=(255, 255, 255))    # fill the inside of the contour with 1

            if area > max_area:
                max_area = area
                biggest = contours[i]
            x, y, w, h = cv2.boundingRect(contours[i])  # gets the coord and size of the bounding box
            offset = 10                                 # offset to make the result image not have the bounding box
            cv2.rectangle(img, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 2)

    kernel = np.ones([7, 7], np.uint8)                  # square 7 by 7 kernel of the number 1

    mask = cv2.erode(mask, kernel, iterations=5)        # remove noise from the mask
    mask = cv2.dilate(mask, kernel, iterations=2)       # expand the masks size to cover the areas the have been erode

    return mask, biggest                                # return the mask and the biggest contour


def image_paths(path, file_type="jpg"):                 # points to a folder and takes all the (default=.jpg) images in it.
    _data = glob.glob(path + "/*." + file_type)         # gets array with \\ as delimiter

    _paths = []
    _names = []
    for file in _data:
        _split_data = file.split("\\")                  # splits the paths over every \\

        _file_path = path + "/" + _split_data[len(_split_data)-1]   # makes a new path with / instead of \\ and the file name.

        _names.append(_split_data[len(_split_data)-1])  # puts the filename in de array of names
        _paths.append(_file_path)                       # puts the new path in the array of paths
    return _paths, _names                               # returns an array of paths and names of the files/images


def image_get(paths):                               # gets the images from a given array of paths
    _images = []
    for i in range(0, len(paths), 1):
        _input_img = cv2.imread(paths[i])
        _input_img = scale_img(_input_img, 0.2)     # scale the images to 20% size to fit them on the screen
        _images.append(_input_img)
    return _images                                  # returns the array with the images


def img_show_all(img, names, destroy=True):  # shows the image array given to it.
    i = 0
    for image in img:                        # Execute for all images
        cv2.imshow(names[i], image)          # make a window with the given name from names and the image to show
        i += 1
    cv2.waitKey(0)                           # wait until te end of time or if a key is pressed
    if destroy:                              # if destroy is true close all the opened opencv windows
        cv2.destroyAllWindows()


def stack_images(scale, imgArray):                  # image scaled and stacked to getter in de form of the arrays dimentions
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]                 # gets the image width
    height = imgArray[0][0].shape[0]                # gets the image width
    if rowsAvailable:                               # gets the image width
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:    # if the hoizontal images array is empty make one
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)  # scale the image
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)  # Put he new col onto the previous
                if len(imgArray[x][y].shape) == 2:                          # if the image is grayscale convert it
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8) # create a new blank image with the total size of the image array
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])                 # put all the image s in the rows together
        ver = np.vstack(hor)                                # put all the new rows together
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def pixel_count(img):   # counts the pixels with values bigger then 0
    pixels = 0
    for v in img:
        for u in v:
            if isinstance(u, int):  # check to see if the variable is an int or a array (gray or color)
                if u > 0:
                    pixels += 1
            else:
                if u.any() > 0:     # in case its a color image if any of the pixels of r,g or b are bigger then 0
                    pixels += 1

    return pixels

