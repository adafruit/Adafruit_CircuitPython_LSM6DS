# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This module provides the ISM330DHCX subclass of LSM6DS for using ISM330DHCX sensors.
"""
from . import LSM6DS, LSM6DS_DEFAULT_ADDRESS, GyroRange


class ISM330DHCX(LSM6DS):  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DS33 6-axis accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the LSM6DS33 is connected to.
        :param address: The I2C slave address of the sensor

    """

    CHIP_ID = 0x6B

    def __init__(self, i2c_bus, address=LSM6DS_DEFAULT_ADDRESS):
        super().__init__(i2c_bus, address)

        # Called DEVICE_CONF in the datasheet, but it recommends setting it
        self._i3c_disable = True

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
