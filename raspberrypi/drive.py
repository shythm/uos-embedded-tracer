import serial

PORT = '/dev/ttyAMA1'
BAUDRATE = 9600

ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

MIN_POWER = 100
MAX_POWER = 255

def set_power(left: int, right: int):
    # map power [0, 255] to [MIN_POWER, MAX_POWER]
    left = int((left - MIN_POWER) / (MAX_POWER - MIN_POWER) * 255)
    right = int((right - MIN_POWER) / (MAX_POWER - MIN_POWER) * 255)

    # the power is between 0 and 255
    left = max(MIN_POWER, left)
    left = min(left, MAX_POWER)
    right = max(MIN_POWER, right)
    right = min(right, MAX_POWER)

    # send command
    cmd = 'L{:+03d}\n'.format(left)
    ser.write(cmd.encode())
    cmd = 'R{:+03d}\n'.format(right)
    ser.write(cmd.encode())
