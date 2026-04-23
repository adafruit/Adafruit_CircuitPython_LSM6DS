# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time

import board

# pylint:disable=no-member
from adafruit_lsm6ds import AccelRange, GyroRange, Rate
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS

# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS
# from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
# from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LSM6DS(i2c)

sensor.accelerometer_range = AccelRange.RANGE_8G
print(f"Accelerometer range set to: {AccelRange.string[sensor.accelerometer_range]:d} G")

sensor.gyro_range = GyroRange.RANGE_2000_DPS
print(f"Gyro range set to: {GyroRange.string[sensor.gyro_range]:d} DPS")

sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
# sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
print(f"Accelerometer rate set to: {Rate.string[sensor.accelerometer_data_rate]:d} HZ")

sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
print(f"Gyro rate set to: {Rate.string[sensor.gyro_data_rate]:d} HZ")

while True:
    print(
        "Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f radians/s"
        % (sensor.acceleration + sensor.gyro)
    )
    time.sleep(0.05)
