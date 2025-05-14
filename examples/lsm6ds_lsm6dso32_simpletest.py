# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time

import board

from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LSM6DSO32(i2c)

while True:
    accel_x, accel_y, accel_z = sensor.acceleration
    print(f"Acceleration: X:{accel_x:.2f}, Y: {accel_y:.2f}, Z: {accel_z:.2f} m/s^2")
    gyro_x, gyro_y, gyro_z = sensor.gyro
    print(f"Gyro X:{gyro_x:.2f}, Y: {gyro_y:.2f}, Z: {gyro_z:.2f} radians/s")
    print("")
    time.sleep(0.5)
