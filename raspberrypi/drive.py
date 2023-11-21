import serial

PORT = '/dev/ttyAMA0'
BAUDRATE = 9600

ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def set_power(left: int, right: int):
    # the power is between 0 and 255
    left = max(0, left)
    left = min(left, 255)
    right = max(0, right)
    right = min(right, 255)

    # send command
    cmd = 'L{:+03d}\n'.format(left)
    ser.write(cmd.encode())
    cmd = 'R{:+03d}\n'.format(right)
    ser.write(cmd.encode())
