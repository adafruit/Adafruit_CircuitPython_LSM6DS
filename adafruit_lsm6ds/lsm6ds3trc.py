# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This module provides the `adafruit_lsm6ds.lsm6ds3trc` subclass of LSM6DS sensors
===============================================================================
"""
from . import LSM6DS, RWBit, const

_LSM6DS_CTRL10_C = const(0x19)


class LSM6DS3TRC(LSM6DS):  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DS3TR-C 6-axis accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the LSM6DS3TR-C is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x6A`


    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`LSM6DS3TRC` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            sensor = LSM6DS3TRC(i2c)

        Now you have access to the :attr:`acceleration` and :attr:`gyro`: attributes

        .. code-block:: python

            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_y, gyro_z = sensor.gyro

    """

    CHIP_ID = 0x6A

    # This version of the IMU has a different register for enabling the pedometer
    # https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf
    _ped_enable = RWBit(_LSM6DS_CTRL10_C, 4)
