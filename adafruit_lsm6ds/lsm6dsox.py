# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This module provides the `adafruit_lsm6ds.lsm6dsox` subclass of LSM6DS sensors
==============================================================================
"""
from . import LSM6DS, LSM6DS_DEFAULT_ADDRESS, LSM6DS_CHIP_ID

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
except ImportError:
    pass


class LSM6DSOX(LSM6DS):  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the LSM6DSOX is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x6A`


    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`LSM6DSOX` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            sensor = LSM6DSOX(i2c)

        Now you have access to the :attr:`acceleration` and :attr:`gyro`: attributes

        .. code-block:: python

            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_z, gyro_z = sensor.gyro

    """

    CHIP_ID = LSM6DS_CHIP_ID

    def __init__(self, i2c_bus: I2C, address: int = LSM6DS_DEFAULT_ADDRESS) -> None:
        super().__init__(i2c_bus, address)
        self._i3c_disable = True
