import board
import busio
#pylint:disable=no-member,unused-import
from adafruit_lsm6ds import LSM6DS33, LSM6DSOX, ISM330DHCT, Rate

i2c = busio.I2C(board.SCL, board.SDA)

sensor = LSM6DS33(i2c)
#sensor = LSM6DSOX(i2c)
#sensor = ISM330DHCT(i2c)

while True:
    sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
    sensor.gyro_data_rate = Rate.RATE_12_5_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sensor.acceleration+sensor.gyro))
    print()

    sensor.accelerometer_data_rate = Rate.RATE_52_HZ
    sensor.gyro_data_rate = Rate.RATE_52_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sensor.acceleration+sensor.gyro))
    print()

    sensor.accelerometer_data_rate = Rate.RATE_416_HZ
    sensor.gyro_data_rate = Rate.RATE_416_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sensor.acceleration+sensor.gyro))
    print()
