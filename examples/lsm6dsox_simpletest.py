import time
import board
import busio
import adafruit_lsm6dsox

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(sox.gyro))
    print("")
    time.sleep(0.5)
