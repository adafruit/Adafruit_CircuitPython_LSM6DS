# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_lsm6ds`
================================================================================

CircuitPython helper library for the LSM6DS family of motion sensors from ST


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* Adafruit LSM6DSOX Breakout <https://www.adafruit.com/products/4438>

* Adafruit ISM330DHCX Breakout <https://www.adafruit.com/product/4502>

* Adafruit LSM6DSO32  Breakout <https://www.adafruit.com/product/4692>

* Adafruit LSM6DS33 Breakout <https://www.adafruit.com/product/4480>

* Adafruit ISM330DHCX + LIS3MDL FEATHERWING <https://www.adafruit.com/product/4569>

* Adafruit LSM6DSOX + LIS3MDL - 9 DOF IMU Breakout <https://www.adafruit.com/product/4517>

* Adafruit LSM6DS33 + LIS3MDL - 9 DOF IMU Breakout <https://www.adafruit.com/product/4485>

* Adafruit LSM6DSOX + LIS3MDL  9 DOF IMU FeatherWing <https://www.adafruit.com/product/4565>

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS.git"

from time import sleep
from math import radians
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit


class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples):
        "creates CV entires"
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value):
        "Returns true if the given value is a member of the CV"
        return value in cls.string


class AccelRange(CV):
    """Options for ``accelerometer_range``"""


class GyroRange(CV):
    """Options for ``gyro_data_range``"""


class Rate(CV):
    """Options for ``accelerometer_data_rate`` and ``gyro_data_rate``"""


Rate.add_values(
    (
        ("RATE_SHUTDOWN", 0, 0, None),
        ("RATE_12_5_HZ", 1, 12.5, None),
        ("RATE_26_HZ", 2, 26.0, None),
        ("RATE_52_HZ", 3, 52.0, None),
        ("RATE_104_HZ", 4, 104.0, None),
        ("RATE_208_HZ", 5, 208.0, None),
        ("RATE_416_HZ", 6, 416.0, None),
        ("RATE_833_HZ", 7, 833.0, None),
        ("RATE_1_66K_HZ", 8, 1066.0, None),
        ("RATE_3_33K_HZ", 9, 3033.0, None),
        ("RATE_6_66K_HZ", 10, 6066.0, None),
        ("RATE_1_6_HZ", 11, 1.6, None),
    )
)


class AccelHPF(CV):
    """Options for the accelerometer high pass filter"""


AccelHPF.add_values(
    (
        ("SLOPE", 0, 0, None),
        ("HPF_DIV100", 1, 0, None),
        ("HPF_DIV9", 2, 0, None),
        ("HPF_DIV400", 3, 0, None),
    )
)


class TapThreshold(CV):
    """Options for the accelerometer tap threshold"""


TapThreshold.add_values(
    (
        ("TAP_THRESHOLD_LOW", 0, 0x01, None),
        ("TAP_THRESHOLD_MID_LOW", 1, 0x08, None),
        ("TAP_THRESHOLD_MID", 2, 0x10, None),
        ("TAP_THRESHOLD_MID_HIGH", 3, 0x18, None),
        ("TAP_THRESHOLD_HIGH", 4, 0x1F, None),
    )
)


class TapShockTime(CV):
    """Options for the accelerometer tap schock time"""


TapShockTime.add_values(
    (
        ("TAP_SHOCK_TIME_LOW", 0, 0x00, None),
        ("TAP_SHOCK_TIME_MID_LOW", 1, 0x01, None),
        ("TAP_SHOCK_TIME_MID_HIGH", 2, 0x02, None),
        ("TAP_SHOCK_TIME_HIGH", 3, 0x03, None),
    )
)

class TapQuietTime(CV):
    """Options for the accelerometer tap quiet time"""


TapQuietTime.add_values(
    (
        ("TAP_QUIET_TIME_LOW", 0, 0x00, None),
        ("TAP_QUIET_TIME_MID_LOW", 1, 0x01, None),
        ("TAP_QUIET_TIME_MID_HIGH", 2, 0x02, None),
        ("TAP_QUIET_TIME_HIGH", 3, 0x03, None),
    )
)


class TapIntPin(CV):
    """Options for the accelerometer tap int pin"""


TapIntPin.add_values(
    (
        ("INT1_PIN", 0, 0x00, None),
        ("INT2_PIN", 1, 0x01, None),
    )
)

LSM6DS_DEFAULT_ADDRESS = const(0x6A)

LSM6DS_CHIP_ID = const(0x6C)

_LSM6DS_WHOAMI = const(0xF)
_LSM6DS_CTRL1_XL = const(0x10)
_LSM6DS_CTRL2_G = const(0x11)
_LSM6DS_CTRL3_C = const(0x12)
_LSM6DS_CTRL8_XL = const(0x17)
_LSM6DS_CTRL9_XL = const(0x18)
_LSM6DS_CTRL10_C = const(0x19)
_LSM6DS_OUT_TEMP_L = const(0x20)
_LSM6DS_OUTX_L_G = const(0x22)
_LSM6DS_OUTX_L_A = const(0x28)
_LSM6DS_STEP_COUNTER = const(0x4B)
_LSM6DS_TAP_CFG = const(0x58)
_LSM6DS_TAP_THS_6D = const(0x59)
_LSM6DS_INT_DUR2 = const(0x5A)
_LSM6DS_MD1_CFG = const(0x5E)
_LSM6DS_MD2_CFG = const(0x5F)

_MILLI_G_TO_ACCEL = 0.00980665


class LSM6DS:  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the LSM6DSOX is connected to.
        :param address: The I2C slave address of the sensor

    """

    # ROUnaryStructs:
    _chip_id = ROUnaryStruct(_LSM6DS_WHOAMI, "<b")

    # Structs
    _raw_accel_data = Struct(_LSM6DS_OUTX_L_A, "<hhh")
    _raw_gyro_data = Struct(_LSM6DS_OUTX_L_G, "<hhh")
    # RWBits:

    _accel_range = RWBits(2, _LSM6DS_CTRL1_XL, 2)
    _accel_data_rate = RWBits(4, _LSM6DS_CTRL1_XL, 4)

    _gyro_data_rate = RWBits(4, _LSM6DS_CTRL2_G, 4)
    _gyro_range = RWBits(2, _LSM6DS_CTRL2_G, 2)
    _gyro_range_125dps = RWBit(_LSM6DS_CTRL2_G, 1)

    _sw_reset = RWBit(_LSM6DS_CTRL3_C, 0)
    _bdu = RWBit(_LSM6DS_CTRL3_C, 6)

    _high_pass_filter = RWBits(2, _LSM6DS_CTRL8_XL, 5)
    _i3c_disable = RWBit(_LSM6DS_CTRL9_XL, 1)
    _pedometer_reset = RWBit(_LSM6DS_CTRL10_C, 1)
    _func_enable = RWBit(_LSM6DS_CTRL10_C, 2)
    _ped_enable = RWBit(_LSM6DS_TAP_CFG, 6)
    _tap_x_enable = RWBit(_LSM6DS_TAP_CFG, 3)
    _tap_y_enable = RWBit(_LSM6DS_TAP_CFG, 2)
    _tap_z_enable = RWBit(_LSM6DS_TAP_CFG, 1)
    _tap_threshold = RWBits(5, _LSM6DS_TAP_THS_6D, 0)
    _tap_shock_time = RWBits(2, _LSM6DS_INT_DUR2, 0)
    _tap_quiet_time = RWBits(2, _LSM6DS_INT_DUR2, 2)
    _single_tap_on_int1_enable = RWBit(_LSM6DS_MD1_CFG, 6)
    _single_tap_on_int2_enable = RWBit(_LSM6DS_MD2_CFG, 6)
    pedometer_steps = ROUnaryStruct(_LSM6DS_STEP_COUNTER, "<h")
    """The number of steps detected by the pedometer. You must enable with `pedometer_enable`
    before calling. Use `pedometer_reset` to reset the number of steps"""
    CHIP_ID = None

    def __init__(self, i2c_bus, address=LSM6DS_DEFAULT_ADDRESS):
        self._cached_accel_range = None
        self._cached_gyro_range = None

        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if self.CHIP_ID is None:
            raise AttributeError("LSM6DS Parent Class cannot be directly instantiated")
        if self._chip_id != self.CHIP_ID:
            raise RuntimeError(
                "Failed to find %s - check your wiring!" % self.__class__.__name__
            )
        self.reset()
        if not hasattr(GyroRange, "string"):
            self._add_gyro_ranges()
        self._bdu = True

        self._add_accel_ranges()
        self.accelerometer_data_rate = Rate.RATE_104_HZ  # pylint: disable=no-member
        self.gyro_data_rate = Rate.RATE_104_HZ  # pylint: disable=no-member

        self.accelerometer_range = AccelRange.RANGE_4G  # pylint: disable=no-member
        self.gyro_range = GyroRange.RANGE_250_DPS  # pylint: disable=no-member

    def reset(self):
        "Resets the sensor's configuration into an initial state"
        self._sw_reset = True
        while self._sw_reset:
            sleep(0.001)

    @staticmethod
    def _add_gyro_ranges():
        GyroRange.add_values(
            (
                ("RANGE_125_DPS", 125, 125, 4.375),
                ("RANGE_250_DPS", 0, 250, 8.75),
                ("RANGE_500_DPS", 1, 500, 17.50),
                ("RANGE_1000_DPS", 2, 1000, 35.0),
                ("RANGE_2000_DPS", 3, 2000, 70.0),
            )
        )

    @staticmethod
    def _add_accel_ranges():
        AccelRange.add_values(
            (
                ("RANGE_2G", 0, 2, 0.061),
                ("RANGE_16G", 1, 16, 0.488),
                ("RANGE_4G", 2, 4, 0.122),
                ("RANGE_8G", 3, 8, 0.244),
            )
        )

    @property
    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2."""
        raw_accel_data = self._raw_accel_data

        x = self._scale_xl_data(raw_accel_data[0])
        y = self._scale_xl_data(raw_accel_data[1])
        z = self._scale_xl_data(raw_accel_data[2])

        return (x, y, z)

    @property
    def gyro(self):
        """The x, y, z angular velocity values returned in a 3-tuple and are in radians / second"""
        raw_gyro_data = self._raw_gyro_data
        x, y, z = [radians(self._scale_gyro_data(i)) for i in raw_gyro_data]
        return (x, y, z)

    def _scale_xl_data(self, raw_measurement):
        return (
            raw_measurement
            * AccelRange.lsb[self._cached_accel_range]
            * _MILLI_G_TO_ACCEL
        )

    def _scale_gyro_data(self, raw_measurement):
        return raw_measurement * GyroRange.lsb[self._cached_gyro_range] / 1000

    @property
    def accelerometer_range(self):
        """Adjusts the range of values that the sensor can measure, from +/- 2G to +/-16G
        Note that larger ranges will be less accurate. Must be an `AccelRange`"""
        return self._cached_accel_range

    # pylint: disable=no-member
    @accelerometer_range.setter
    def accelerometer_range(self, value):
        if not AccelRange.is_valid(value):
            raise AttributeError("range must be an `AccelRange`")
        self._accel_range = value
        self._cached_accel_range = value
        sleep(0.2)  # needed to let new range settle

    @property
    def gyro_range(self):
        """Adjusts the range of values that the sensor can measure, from 125 Degrees/s to 2000
        degrees/s. Note that larger ranges will be less accurate. Must be a `GyroRange`."""
        return self._cached_gyro_range

    @gyro_range.setter
    def gyro_range(self, value):
        self._set_gyro_range(value)
        sleep(0.2)

    def _set_gyro_range(self, value):
        if not GyroRange.is_valid(value):
            raise AttributeError("range must be a `GyroRange`")

        # range uses `FS_G` enum
        if value <= GyroRange.RANGE_2000_DPS:  # pylint: disable=no-member
            self._gyro_range_125dps = False
            self._gyro_range = value
        # range uses the `FS_125` bit
        if value is GyroRange.RANGE_125_DPS:  # pylint: disable=no-member
            self._gyro_range_125dps = True

        self._cached_gyro_range = value  # needed to let new range settle

    @property
    def accelerometer_data_rate(self):
        """Select the rate at which the accelerometer takes measurements. Must be a `Rate`"""
        return self._accel_data_rate

    @accelerometer_data_rate.setter
    def accelerometer_data_rate(self, value):

        if not Rate.is_valid(value):
            raise AttributeError("accelerometer_data_rate must be a `Rate`")

        self._accel_data_rate = value
        # sleep(.2) # needed to let new range settle

    @property
    def gyro_data_rate(self):
        """Select the rate at which the gyro takes measurements. Must be a `Rate`"""
        return self._gyro_data_rate

    @gyro_data_rate.setter
    def gyro_data_rate(self, value):
        if not Rate.is_valid(value):
            raise AttributeError("gyro_data_rate must be a `Rate`")

        self._gyro_data_rate = value
        # sleep(.2) # needed to let new range settle

    @property
    def tap_x_enable(self):
        """ Whether the tap on x axis on the accelerometer is enabled"""
        return self._tap_x_enable

    # pylint: disable=no-member
    @tap_x_enable.setter
    def tap_x_enable(self, enable):
        self._tap_x_enable = enable
        #sleep(0.2)  # needed to let enable/disable settle

    @property
    def tap_y_enable(self):
        """ Whether the tap on y axis on the accelerometer is enabled"""
        return self._tap_y_enable

    # pylint: disable=no-member
    @tap_y_enable.setter
    def tap_y_enable(self, enable):
        self._tap_y_enable = enable
        #sleep(0.2)  # needed to let enable/disable settle

    @property
    def tap_z_enable(self):
        """ Whether the tap on z axis on the accelerometer is enabled"""
        return self._tap_z_enable

    # pylint: disable=no-member
    @tap_z_enable.setter
    def tap_z_enable(self, enable):
        self._tap_z_enable = enable
        #sleep(0.2)  # needed to let enable/disable settle

    @property
    def tap_threshold(self):
        """ Current value for the tap threshold on the accelerometer"""
        return self._tap_threshold
    # pylint: disable=no-member

    @tap_threshold.setter
    def tap_threshold(self, value):
        if not TapThreshold.is_valid(value):
            raise AttributeError("tap threshold must be a `TapThreshold`")
        self._tap_threshold = value
        #sleep(.2) # needed to let new threshold settle

    @property
    def tap_quiet_time(self):
        """ Current value for the tap quiet time on the accelerometer"""
        return self._tap_quiet_time

    @tap_quiet_time.setter
    def tap_quiet_time(self, value):
        if not TapQuietTime.is_valid(value):
            raise AttributeError("tap threshold must be a `TapQuietTime`")

        self._tap_quiet_time = value
        #sleep(.2) # needed to let new shock time settle

    @property
    def tap_shock_time(self):
        """ Current value for the tap shock time on the accelerometer"""
        return self._tap_shock_time

    @tap_shock_time.setter
    def tap_shock_time(self, value):
        if not TapShockTime.is_valid(value):
            raise AttributeError("tap threshold must be a `TapShockTime`")

        self._tap_shock_time = value
        #sleep(.2) # needed to let new shock time settle

    @property
    def single_tap_on_int1_enable(self):
        """ Whether the single tap on int1 on the accelerometer is enabled"""
        return self._single_tap_on_int1_enable

    @single_tap_on_int1_enable.setter
    def single_tap_on_int1_enable(self, enable):
        self._single_tap_on_int1_enable = enable

    @property
    def single_tap_on_int2_enable(self):
        """ Whether the single tap on int2 on the accelerometer is enabled"""
        return self._single_tap_on_int2_enable

    @single_tap_on_int2_enable.setter
    def single_tap_on_int2_enable(self, enable):
        self._single_tap_on_int2_enable = enable

    @property
    def pedometer_enable(self):
        """ Whether the pedometer function on the accelerometer is enabled"""
        return self._ped_enable and self._func_enable

    @pedometer_enable.setter
    def pedometer_enable(self, enable):
        self._ped_enable = enable
        self._func_enable = enable
        self._pedometer_reset = enable

    @property
    def is_single_tap_detection_enable(self):
        """ Whether the single tap function on the accelerometer is enabled"""
        return (self._tap_x_enable or self._tap_y_enable or self._tap_z_enable) and (self._single_tap_on_int1_enable or self._single_tap_on_int2_enable)# pylint: disable=line-too-long

    def single_tap_detection_enable(self, enable, axis_enable='xyz', int_pin=TapIntPin.INT1_PIN, threshold=TapThreshold.TAP_THRESHOLD_MID_LOW, data_rate=Rate.RATE_1_66K_HZ, accel_range=0, shock_time=TapShockTime.TAP_SHOCK_TIME_MID_HIGH, quiet_time=TapQuietTime.TAP_QUIET_TIME_MID_LOW):
        """Enable or disable the single tap detection on the accelerometer"""
        #Set_X_ODR(416.0f)
        self.accelerometer_data_rate = data_rate
        #Set_X_FS(2.0f)
        self.accelerometer_range = accel_range
        #LSM6DS3_ACC_GYRO_W_TAP_X_EN
        self.tap_x_enable = 'x' in axis_enable
        #LSM6DS3_ACC_GYRO_W_TAP_Y_EN
        self.tap_y_enable = 'y' in axis_enable
        #LSM6DS3_ACC_GYRO_W_TAP_Z_EN
        self.tap_z_enable = 'z' in axis_enable
        #Set_Tap_Threshold
        self.tap_threshold = threshold
        #Set_Tap_Shock_Time
        self.tap_shock_time = shock_time
        #Set_Tap_Quiet_Time
        self.tap_quiet_time = quiet_time
        if not TapIntPin.is_valid(int_pin):
            raise AttributeError("tap int pin must be a `TapIntPin`")

        if int_pin == TapIntPin.INT1_PIN:
            self.single_tap_on_int1_enable = enable
        else:
            self.single_tap_on_int2_enable = enable

    @property
    def high_pass_filter(self):
        """The high pass filter applied to accelerometer data"""
        return self._high_pass_filter

    @high_pass_filter.setter
    def high_pass_filter(self, value):
        if not AccelHPF.is_valid(value):
            raise AttributeError("range must be an `AccelHPF`")
        self._high_pass_filter = value
