import numpy as np
import cv2

base_line = 0.5
WIDTH = 40
HEIGHT = 30

prev_pos = -1

def sense_line(img):
    global prev_pos

    # resize image
    img = cv2.resize(img, (WIDTH, HEIGHT))

    # convert to gray scale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # binarization
    threshold_value = 128
    _, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)

    # draw horizontal line
    cv2.line(img, (0, int(HEIGHT * base_line)), (WIDTH, int(HEIGHT * base_line)), (255, 255, 0), 1)

    # get base line array
    base_line_array = 255 - binary_image[int(HEIGHT * base_line), :]
    
    # get position
    detected = np.where(base_line_array > 0)
    if (detected[0].size == 0):
        detected = prev_pos
    else:
        detected = (np.mean(detected) - (WIDTH / 2)) / (WIDTH / 2)
        prev_pos = detected

    return detected, img
