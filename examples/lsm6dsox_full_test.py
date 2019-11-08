import time
import board
import busio
from adafruit_lsm6dsox import LSM6DSOX, Rate, AccelRange, GyroRange

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

print()
for accel_range in [AccelRange.RANGE_2G, AccelRange.RANGE_4G,
    AccelRange.RANGE_8G, AccelRange.RANGE_16G]:

    sox.accelerometer_range = accel_range
    print("Gravity is %.2f ms^2 when accelerometer range is %d G"%
        (sox.acceleration[2], AccelRange.string[sox.accelerometer_range]))

print()
for gyro_range in [GyroRange.RANGE_250_DPS, GyroRange.RANGE_500_DPS,
    GyroRange.RANGE_1000_DPS, GyroRange.RANGE_2000_DPS]:

    sox.gyro_range = gyro_range
    print("Non movement is %.2f degrees/s when gyro range is %d DPS"%
        (sox.gyro[2], GyroRange.string[sox.gyro_range]))

while True:
    print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s"%
        (sox.acceleration+sox.gyro))