import time
import board
import busio
#pylint:disable=no-member,unused-import
from adafruit_lsm6ds import LSM6DS33, LSM6DSOX, ISM330DHCT, Rate, AccelRange, GyroRange

i2c = busio.I2C(board.SCL, board.SDA)

sensor = LSM6DS33(i2c)
#sensor = LSM6DSOX(i2c)
#sensor = ISM330DHCT(i2c)

sensor.accelerometer_range = AccelRange.RANGE_8G
print("Accelerometer range set to: %d G" % AccelRange.string[sensor.accelerometer_range])

sensor.gyro_range = GyroRange.RANGE_2000_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[sensor.gyro_range])

sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
#sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
print("Accelerometer rate set to: %d HZ" % Rate.string[sensor.accelerometer_data_rate])

sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
print("Gyro rate set to: %d HZ" % Rate.string[sensor.gyro_data_rate])

while True:
    print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s" %
          (sensor.acceleration+sensor.gyro))
    time.sleep(0.05)
