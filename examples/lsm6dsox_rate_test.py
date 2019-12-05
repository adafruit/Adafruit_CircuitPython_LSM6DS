import board
import busio
import adafruit_lsm6dsox
#pylint:disable=no-member

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)

while True:
    sox.accelerometer_data_rate = adafruit_lsm6dsox.Rate.RATE_12_5_HZ
    sox.gyro_data_rate = adafruit_lsm6dsox.Rate.RATE_12_5_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sox.acceleration+sox.gyro))
    print()

    sox.accelerometer_data_rate = adafruit_lsm6dsox.Rate.RATE_52_HZ
    sox.gyro_data_rate = adafruit_lsm6dsox.Rate.RATE_52_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sox.acceleration+sox.gyro))
    print()

    sox.accelerometer_data_rate = adafruit_lsm6dsox.Rate.RATE_416_HZ
    sox.gyro_data_rate = adafruit_lsm6dsox.Rate.RATE_416_HZ
    for i in range(100):
        print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f"%(sox.acceleration+sox.gyro))
    print()
