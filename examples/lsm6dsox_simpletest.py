import time
import board
import busio
import adafruit_lsm6dsox

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)
