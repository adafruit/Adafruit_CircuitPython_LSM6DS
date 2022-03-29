# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_lsm6ds`
================================================================================

CircuitPython helper library for the LSM6DS family of motion sensors from ST


* Author(s): Bryan Siepert, Jose David M.

Implementation Notes
--------------------

**Hardware:**

* `Adafruit LSM6DSOX 6 DoF Accelerometer and Gyroscope
  <https://www.adafruit.com/product/4438>`_ (Product ID: 4438)

* `Adafruit ISM330DHCX - 6 DoF IMU - Accelerometer and Gyroscope
  <https://www.adafruit.com/product/4502>`_ (Product ID: 4502)

* `Adafruit LSM6DSO32 6-DoF Accelerometer and Gyroscope
  <https://www.adafruit.com/product/4692>`_ (Product ID: 4692)

* `Adafruit LSM6DS33 6-DoF Accel + Gyro IMU
  <https://www.adafruit.com/product/4480>`_ (Product ID: 4480)

* `Adafruit ISM330DHCX + LIS3MDL FeatherWing - High Precision 9-DoF IMU
  <https://www.adafruit.com/product/4569>`_ (Product ID: 4569)

* `Adafruit LSM6DSOX + LIS3MDL - Precision 9 DoF IMU
  <https://www.adafruit.com/product/4517>`_ (Product ID: 4517)

* `Adafruit LSM6DS33 + LIS3MDL - 9 DoF IMU with Accel / Gyro / Mag
  <https://www.adafruit.com/product/4485>`_ (Product ID: 4485)

* `Adafruit LSM6DSOX + LIS3MDL FeatherWing - Precision 9-DoF IMU
  <https://www.adafruit.com/product/4565>`_ (Product ID: 4565)


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS.git"

import struct
from time import sleep
from math import radians
from micropython import const
from adafruit_bus_device import i2c_device

from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

try:
    from typing import Tuple, Optional
    from busio import I2C
except ImportError:
    pass


class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples: Tuple[str, int, float, Optional[float]]) -> None:
        "creates CV entires"
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value: int) -> bool:
        """Returns true if the given value is a member of the CV"""
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

LSM6DS_DEFAULT_ADDRESS = const(0x6A)

LSM6DS_CHIP_ID = const(0x6C)

_LSM6DS_MLC_INT1 = const(0x0D)
_LSM6DS_WHOAMI = const(0xF)
_LSM6DS_CTRL1_XL = const(0x10)
_LSM6DS_CTRL2_G = const(0x11)
_LSM6DS_CTRL3_C = const(0x12)
_LSM6DS_CTRL8_XL = const(0x17)
_LSM6DS_CTRL9_XL = const(0x18)
_LSM6DS_CTRL10_C = const(0x19)
_LSM6DS_ALL_INT_SRC = const(0x1A)
_LSM6DS_OUT_TEMP_L = const(0x20)
_LSM6DS_OUTX_L_G = const(0x22)
_LSM6DS_OUTX_L_A = const(0x28)
_LSM6DS_MLC_STATUS = const(0x38)
_LSM6DS_STEP_COUNTER = const(0x4B)
_LSM6DS_TAP_CFG0 = const(0x56)
_LSM6DS_TAP_CFG = const(0x58)
_LSM6DS_MLC0_SRC = const(0x70)
_MILLI_G_TO_ACCEL = 0.00980665
_TEMPERATURE_SENSITIVITY = 256
_TEMPERATURE_OFFSET = 25.0

_LSM6DS_EMB_FUNC_EN_A = const(0x04)
_LSM6DS_EMB_FUNC_EN_B = const(0x05)
_LSM6DS_FUNC_CFG_ACCESS = const(0x01)
_LSM6DS_FUNC_CFG_BANK_USER = const(0)
_LSM6DS_FUNC_CFG_BANK_HUB = const(1)
_LSM6DS_FUNC_CFG_BANK_EMBED = const(2)


class LSM6DS:  # pylint: disable=too-many-instance-attributes

    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the LSM6DSOX is connected to.
    :param int address: TThe I2C device address. Defaults to :const:`0x6A`

    """

    # ROUnaryStructs:
    _chip_id = ROUnaryStruct(_LSM6DS_WHOAMI, "<b")

    # Structs
    _raw_accel_data = Struct(_LSM6DS_OUTX_L_A, "<hhh")
    _raw_gyro_data = Struct(_LSM6DS_OUTX_L_G, "<hhh")
    _raw_temp_data = Struct(_LSM6DS_OUT_TEMP_L, "<h")
    _emb_func_en_a = Struct(_LSM6DS_EMB_FUNC_EN_A, "<b")
    _emb_func_en_b = Struct(_LSM6DS_EMB_FUNC_EN_B, "<b")
    _mlc0_src = Struct(_LSM6DS_MLC0_SRC, "<bbbbbbbb")
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
    _mem_bank = RWBit(_LSM6DS_FUNC_CFG_ACCESS, 7)
    _mlc_status = ROBit(_LSM6DS_MLC_STATUS, 0)
    _i3c_disable = RWBit(_LSM6DS_CTRL9_XL, 0)
    _block_data_enable = RWBit(_LSM6DS_CTRL3_C, 4)
    _route_int1 = RWBit(_LSM6DS_MLC_INT1, 0)
    _tap_latch = RWBit(_LSM6DS_TAP_CFG0, 0)
    _tap_clear = RWBit(_LSM6DS_TAP_CFG0, 6)
    _ped_enable = RWBit(_LSM6DS_TAP_CFG, 6)
    pedometer_steps = ROUnaryStruct(_LSM6DS_STEP_COUNTER, "<h")
    """The number of steps detected by the pedometer. You must enable with `pedometer_enable`
    before calling. Use ``pedometer_reset`` to reset the number of steps"""
    CHIP_ID = None

    def __init__(
        self, i2c_bus: I2C, address: int = LSM6DS_DEFAULT_ADDRESS, ucf: str = None
    ) -> None:
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
        # Load and configure MLC if UCF file is provided
        if ucf is not None:
            self.load_mlc(ucf)

    def reset(self) -> None:
        "Resets the sensor's configuration into an initial state"
        self._sw_reset = True
        while self._sw_reset:
            sleep(0.001)

    @staticmethod
    def _add_gyro_ranges() -> None:
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
    def _add_accel_ranges() -> None:
        AccelRange.add_values(
            (
                ("RANGE_2G", 0, 2, 0.061),
                ("RANGE_16G", 1, 16, 0.488),
                ("RANGE_4G", 2, 4, 0.122),
                ("RANGE_8G", 3, 8, 0.244),
            )
        )

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2."""
        raw_accel_data = self._raw_accel_data

        x = self._scale_xl_data(raw_accel_data[0])
        y = self._scale_xl_data(raw_accel_data[1])
        z = self._scale_xl_data(raw_accel_data[2])

        return (x, y, z)

    @property
    def gyro(self) -> Tuple[float, float, float]:
        """The x, y, z angular velocity values returned in a 3-tuple and are in radians / second"""
        raw_gyro_data = self._raw_gyro_data
        x, y, z = [radians(self._scale_gyro_data(i)) for i in raw_gyro_data]
        return (x, y, z)

    def _scale_xl_data(self, raw_measurement: int) -> float:
        return (
            raw_measurement
            * AccelRange.lsb[self._cached_accel_range]
            * _MILLI_G_TO_ACCEL
        )

    def _scale_gyro_data(self, raw_measurement: int) -> float:
        return raw_measurement * GyroRange.lsb[self._cached_gyro_range] / 1000

    @property
    def accelerometer_range(self) -> int:
        """Adjusts the range of values that the sensor can measure, from +/- 2G to +/-16G
        Note that larger ranges will be less accurate. Must be an ``AccelRange``"""
        return self._cached_accel_range

    # pylint: disable=no-member
    @accelerometer_range.setter
    def accelerometer_range(self, value: int) -> None:
        if not AccelRange.is_valid(value):
            raise AttributeError("range must be an `AccelRange`")
        self._accel_range = value
        self._cached_accel_range = value
        sleep(0.2)  # needed to let new range settle

    @property
    def gyro_range(self) -> int:
        """Adjusts the range of values that the sensor can measure, from 125 Degrees/s to 2000
        degrees/s. Note that larger ranges will be less accurate. Must be a ``GyroRange``."""
        return self._cached_gyro_range

    @gyro_range.setter
    def gyro_range(self, value: int) -> None:
        self._set_gyro_range(value)
        sleep(0.2)

    def _set_gyro_range(self, value: int) -> None:
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
    def accelerometer_data_rate(self) -> int:
        """Select the rate at which the accelerometer takes measurements. Must be a ``Rate``"""
        return self._accel_data_rate

    @accelerometer_data_rate.setter
    def accelerometer_data_rate(self, value: int) -> None:

        if not Rate.is_valid(value):
            raise AttributeError("accelerometer_data_rate must be a `Rate`")

        self._accel_data_rate = value
        # sleep(.2) # needed to let new range settle

    @property
    def gyro_data_rate(self) -> int:
        """Select the rate at which the gyro takes measurements. Must be a ``Rate``"""
        return self._gyro_data_rate

    @gyro_data_rate.setter
    def gyro_data_rate(self, value: int) -> None:
        if not Rate.is_valid(value):
            raise AttributeError("gyro_data_rate must be a `Rate`")

        self._gyro_data_rate = value
        # sleep(.2) # needed to let new range settle

    @property
    def pedometer_enable(self) -> bool:
        """Whether the pedometer function on the accelerometer is enabled"""
        return self._ped_enable and self._func_enable

    @pedometer_enable.setter
    def pedometer_enable(self, enable: bool) -> None:
        self._ped_enable = enable
        self._func_enable = enable
        self._pedometer_reset = enable

    @property
    def high_pass_filter(self) -> int:
        """The high pass filter applied to accelerometer data"""
        return self._high_pass_filter

    @high_pass_filter.setter
    def high_pass_filter(self, value: int) -> None:
        if not AccelHPF.is_valid(value):
            raise AttributeError("range must be an `AccelHPF`")
        self._high_pass_filter = value

    @property
    def temperature(self) -> float:
        """Temperature in Celsius"""
        # Data from Datasheet Table 4.3
        # Temp range -40 to 85 Celsius
        # T_ADC_RES = ADC Res 16 bit
        # Stabilization time 500 μs

        temp = self._raw_temp_data[0]

        return temp / _TEMPERATURE_SENSITIVITY + _TEMPERATURE_OFFSET

    def _set_embedded_functions(self, enable, emb_ab=None):
        """Enable/disable embedded functions - returns prior settings when disabled"""
        self._mem_bank = 1
        if enable:
            self._emb_func_en_a = emb_ab[0]
            self._emb_func_en_b = emb_ab[1]
        else:
            emb_a = self._emb_func_en_a
            emb_b = self._emb_func_en_b
            self._emb_func_en_a = (emb_a[0] & 0xC7,)
            self._emb_func_en_b = (emb_b[0] & 0xE6,)
            emb_ab = (emb_a, emb_b)

        self._mem_bank = 0
        return emb_ab

    def load_mlc(self, ucf):
        """Load MLC configuration file into sensor"""
        buf = bytearray(2)
        with self.i2c_device as i2c:
            # Load MLC config from file
            with open(ucf, "r") as ucf_file:
                for line in ucf_file:
                    if line.startswith("Ac"):
                        command = [int(v, 16) for v in line.strip().split(" ")[1:3]]
                        buf[0] = command[0]
                        buf[1] = command[1]
                        i2c.write(buf)

        # Disable embudded function -- save current settings
        emb_ab = self._set_embedded_functions(False)

        # Disable I3C interface
        self._i3c_disable = 1

        # Enable Block Data Update
        self._block_data_enable = 1

        # Route signals on interrupt pin 1
        self._mem_bank = 1
        self._route_int1 &= 1
        self._mem_bank = 0

        # Configure interrupt pin mode
        self._tap_latch = 1
        self._tap_clear = 1

        # Enabble Embedded Functions using previously stored settings
        self._set_embedded_functions(True, emb_ab)

    def read_mlc_output(self):
        """Read MLC results"""
        buf = None
        if self._mlc_status:
            self._mem_bank = 1
            buf = self._mlc0_src
            self._mem_bank = 0
        return buf
