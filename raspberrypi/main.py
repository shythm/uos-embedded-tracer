from picamera2 import Picamera2
import cv2
import sensing
import drive

picam2 = Picamera2()
# picam2.create_preview_configuration({ "format": "YUV420" })
video_config = picam2.create_video_configuration({
    'format': 'RGB888',
    'size': (200, 150),
})
picam2.configure(video_config)
picam2.start()

power = 50

while True:
    # get image from pi camera
    im = picam2.capture_array()
    
    # rotate 180
    im = cv2.rotate(im, cv2.ROTATE_180)

    # line sensing
    pos, im = sensing.sense_line(im)

    # motor speed control
    # drive.set_power(100, 200)
    print(pos)
    drive.set_power(int(power * (1 + pos)), int(power * (1 - pos)))

    cv2.imshow("Camera", im)
    cv2.waitKey(1)
