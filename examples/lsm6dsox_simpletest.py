import time
import board
import busio
import adafruit_lsm6dsox
from adafruit_debug_i2c import DebugI2C

i2c = busio.I2C(board.SCL, board.SDA)
# i2c = DebugI2C(busio.I2C(board.SCL, board.SDA))

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)
sox.gyro_range = adafruit_lsm6dsox.GyroRange.RANGE_1000_DPS
sox.range = adafruit_lsm6dsox.AccelRange.RANGE_16G
sox.gyro_data_rate = adafruit_lsm6dsox.Rate.RATE_12_5_HZ
sox.data_rate = adafruit_lsm6dsox.Rate.RATE_12_5_HZ
for i in range(50):
# while True:
    # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(sox.gyro))
    # print("Temperature: %.2f C"%sox._raw_temp)
    # print("")
    print("(%.2f, %.2f, %.2f)"%(sox.acceleration))
    print("(%.2f, %.2f, %.2f)"%(sox.gyro))
    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(sox.gyro))
    # print("Temperature: %.2f C"%sox._raw_temp)
    # print("")
    time.sleep(0.01)
