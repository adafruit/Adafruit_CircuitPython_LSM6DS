import board
import busio
from adafruit_lsm6dsox import LSM6DSOX, Rate, AccelRange, GyroRange
#pylint:disable=no-member
i2c = busio.I2C(board.SCL, board.SDA)
sox = LSM6DSOX(i2c)

sox.accelerometer_range = AccelRange.RANGE_16G
print("Accelerometer range set to: %d G"%AccelRange.string[sox.accelerometer_range])

sox.gyro_range = GyroRange.RANGE_500_DPS
print("Gyro range set to: %d DPS"%GyroRange.string[sox.gyro_range])

sox.accelerometer_rate = Rate.RATE_12_5_HZ
print("Accelerometer rate set to: %d HZ"%Rate.string[sox.accelerometer_rate])

sox.gyro_rate = Rate.RATE_12_5_HZ
print("Gyro rate set to: %d HZ"%Rate.string[sox.gyro_rate])

while True:
    print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s"%
          (sox.acceleration+sox.gyro))
