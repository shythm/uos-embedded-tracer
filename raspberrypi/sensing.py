import numpy as np
import cv2
import math

SCALEDOWN_WIDTH = 40
SCALEDOWN_HEIGHT = 30
BINARY_THRESHOLD = 128
BASE_LINE = int(SCALEDOWN_HEIGHT * 0.5)

def sense_line(img):
    # resize image
    img = cv2.resize(img, (SCALEDOWN_WIDTH, SCALEDOWN_HEIGHT))

    # convert to gray scale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # binarization
    _, binary_image = cv2.threshold(gray_image, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

    # get base line array
    base_line_array = 255 - binary_image[BASE_LINE, :]
    
    # draw horizontal line (for debug)
    cv2.line(img, (0, BASE_LINE), (SCALEDOWN_WIDTH, BASE_LINE), (255, 255, 0), 1)

    # get position array
    pos_arr = base_line_array > 0

    # get next position
    pos = _get_next_position(pos_arr)

    return pos, img

prev_pos = -1
score_threshold = SCALEDOWN_WIDTH * 0.2

def _get_next_position(self, arr):
    max_score = -math.inf
    max_pos = -1

    for pos, detected in enumerate(arr):
        if detected:
            # calculate hueristic score
            score = -abs(self.prev_pos - pos)
            if score > max_score:
                max_score = score
                max_pos = pos

    if max_pos == -1 or max_score < self.score_threshold:
        # no line detected or detected line is too far
        max_pos = self.prev_pos

    self.prev_pos = max_pos # update prev_pos
    return max_pos
