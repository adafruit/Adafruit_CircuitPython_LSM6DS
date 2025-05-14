# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time

import board
import busio
import digitalio

from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

# On the Seeed XIAO nRF52840 Sense the LSM6DS3TR-C IMU is connected on a separate
# I2C bus and it has its own power pin that we need to enable.
imupwr = digitalio.DigitalInOut(board.IMU_PWR)
imupwr.direction = digitalio.Direction.OUTPUT
imupwr.value = True
time.sleep(0.1)

imu_i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
sensor = LSM6DS3TRC(imu_i2c)

while True:
    accel_x, accel_y, accel_z = sensor.acceleration
    print(f"Acceleration: X:{accel_x:.2f}, Y: {accel_y:.2f}, Z: {accel_z:.2f} m/s^2")
    gyro_x, gyro_y, gyro_z = sensor.gyro
    print(f"Gyro X:{gyro_x:.2f}, Y: {gyro_y:.2f}, Z: {gyro_z:.2f} radians/s")
    print("")
    time.sleep(0.5)
