import time
import board
import busio
from adafruit_lsm6ds import LSM6DSO32

i2c = busio.I2C(board.SCL, board.SDA)
sensor = LSM6DSO32(i2c)
while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
    print("")
    time.sleep(0.5)
