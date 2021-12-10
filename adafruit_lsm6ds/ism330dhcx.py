# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This module provides the `adafruit_lsm6ds.ism330dhcx` subclass of LSM6DS sensors
==================================================================================
"""
from time import sleep
from . import LSM6DS, LSM6DS_DEFAULT_ADDRESS, GyroRange, RWBit, const

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
except ImportError:
    pass

_LSM6DS_CTRL2_G = const(0x11)


class ISM330DHCX(LSM6DS):  # pylint: disable=too-many-instance-attributes

    """Driver for the ISM330DHCX 6-axis accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the device is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x6A`


    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`ISM330DHCX` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            sensor = ISM330DHCX(i2c)

        Now you have access to the :attr:`acceleration` and :attr:`gyro`: attributes

        .. code-block:: python

            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_z, gyro_z = sensor.gyro


    """

    CHIP_ID = 0x6B
    _gyro_range_4000dps = RWBit(_LSM6DS_CTRL2_G, 0)

    def __init__(self, i2c_bus: I2C, address: int = LSM6DS_DEFAULT_ADDRESS) -> None:
        GyroRange.add_values(
            (
                ("RANGE_125_DPS", 125, 125, 4.375),
                ("RANGE_250_DPS", 0, 250, 8.75),
                ("RANGE_500_DPS", 1, 500, 17.50),
                ("RANGE_1000_DPS", 2, 1000, 35.0),
                ("RANGE_2000_DPS", 3, 2000, 70.0),
                ("RANGE_4000_DPS", 4000, 4000, 140.0),
            )
        )
        super().__init__(i2c_bus, address)

        # Called DEVICE_CONF in the datasheet, but it recommends setting it
        self._i3c_disable = True

    @property
    def gyro_range(self) -> int:
        """Adjusts the range of values that the sensor can measure, from 125 Degrees/s to 4000
        degrees/s. Note that larger ranges will be less accurate. Must be a ``GyroRange``. 4000 DPS
        is only available for the ISM330DHCX"""
        return self._cached_gyro_range

    @gyro_range.setter
    def gyro_range(self, value: int) -> None:
        super()._set_gyro_range(value)

        # range uses the `FS_4000` bit
        if value is GyroRange.RANGE_4000_DPS:  # pylint: disable=no-member
            self._gyro_range_125dps = False
            self._gyro_range_4000dps = True
        else:
            self._gyro_range_4000dps = False

        sleep(0.2)  # needed to let new range settle
