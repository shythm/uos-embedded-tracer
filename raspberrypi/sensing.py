import numpy as np
import cv2
import math

SCALEDOWN_WIDTH = 40
SCALEDOWN_HEIGHT = 30
BINARY_THRESHOLD = 128
BASE_LINE = int(SCALEDOWN_HEIGHT * 0.5)

def _get_pos_arr(img):
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

    return img, pos_arr

_prev_pos = -1

def _get_next_position_immediate(pos_arr) -> int:
    global _prev_pos
    
    detected = np.where(pos_arr)
    if detected[0].size == 0:
        # no line detected
        return _prev_pos
    else:
        # get mean of detected positions
        mean_pos = int(np.mean(detected))
        _prev_pos = mean_pos
        return mean_pos

SCORE_THRESHOLD = SCALEDOWN_WIDTH * 0.2

def _get_next_position_hueristic(pos_arr) -> int:
    global _prev_pos

    max_score = -math.inf
    max_pos = -1

    for pos, detected in enumerate(pos_arr):
        if detected:
            # calculate hueristic score
            score = -abs(_prev_pos - pos)
            if score > max_score:
                max_score = score
                max_pos = pos

    if max_pos == -1 or max_score < SCORE_THRESHOLD:
        # no line detected or detected line is too far
        max_pos = _prev_pos

    _prev_pos = max_pos # update prev_pos
    return max_pos

def sense_line(img, method) -> float:
    im, pos_arr = _get_pos_arr(img)

    if method == 'immediate':
        pos = _get_next_position_immediate(pos_arr)
    elif method == 'hueristic':
        pos = _get_next_position_hueristic(pos_arr)
    else:
        raise ValueError('Invalid method')

    # centering
    pos = (pos - SCALEDOWN_WIDTH * 0.5) / (SCALEDOWN_WIDTH * 0.5)

    return im, pos
