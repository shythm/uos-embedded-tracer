from picamera2 import Picamera2
import cv2
import sensing
import drive

def main():
    # camera initialization
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration({
        'format': 'RGB888',
        'size': (200, 150),
    })
    picam2.configure(video_config)
    picam2.start()

    # constants initialization
    POWER = 50
    K_P = 0.50

    # driving loop
    while True:
        # get image from pi camera
        im = picam2.capture_array()

        # line sensing
        im, pos = sensing.sense_line(im, 'immediate')
        
        left = int(POWER * (1 + K_P * pos))
        right = int(POWER * (1 - K_P * pos))
        
        drive.set_power(left, right)

        im = cv2.resize(im, (400, 300))

        cv2.imshow("Camera", im)
        cv2.waitKey(33) # delay 33ms

def final():
    drive.set_power(0, 0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        final()
