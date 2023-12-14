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

DEAD_ZONE_LEFT = 38
DEAD_ZONE_RIGHT = 30
MAX_POWER = 255

def set_power_off():
    # send command
    cmd = 'L+000\nR+000\n'.format()
    ser.write(cmd.encode())

def set_power(left: int, right: int):
    # 1. map power [0, 255] to [MIN_POWER, MAX_POWER]
    # 2. limit power [0, 255]

    if left > DEAD_ZONE_LEFT:
        left = int((left - DEAD_ZONE_LEFT) / (MAX_POWER - DEAD_ZONE_LEFT) * 255)
        left = max(DEAD_ZONE_LEFT, left)
        left = min(left, MAX_POWER)
    else:
        left = DEAD_ZONE_LEFT

    if right > DEAD_ZONE_RIGHT:
        right = int((right - DEAD_ZONE_RIGHT) / (MAX_POWER - DEAD_ZONE_RIGHT) * 255)
        right = max(DEAD_ZONE_RIGHT, right)
        right = min(right, MAX_POWER)
    else:
        right = DEAD_ZONE_RIGHT

    # send command
    cmd = 'L{:+03d}\n'.format(left)
    ser.write(cmd.encode())
    cmd = 'R{:+03d}\n'.format(right)
    ser.write(cmd.encode())
