# SPDX-FileCopyrightText: Copyright (c) 2022 Edrig
#
# SPDX-License-Identifier: MIT
"""
This module provides the `adafruit_lsm6ds.lsm6ds33` subclass of LSM6DS sensors
===============================================================================
"""
from . import LSM6DS


class LSM6DS3(LSM6DS):  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DS3 6-axis accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the LSM6DS3 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x6A`


    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`LSM6DS3` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            sensor = LSM6DS3(i2c)

        Now you have access to the :attr:`acceleration` and :attr:`gyro`: attributes

        .. code-block:: python

            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_z, gyro_z = sensor.gyro

    """

    CHIP_ID = 0x6A
