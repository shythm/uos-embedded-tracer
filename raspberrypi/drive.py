import serial

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def set_power(left, right):
    cmd = 'L{:+03d}\n'.format(left)
    ser.write(cmd.encode())
    cmd = 'R{:+03d}\n'.format(right)
    ser.write(cmd.encode())
