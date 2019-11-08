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
`adafruit_lsm6dsox`
================================================================================

CircuitPython library for the ST LSM6DSOX 6-axis Accelerometer and Gyro


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX.git"
from time import sleep
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct, Struct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX.git"


_LSM6DSOX_DEFAULT_ADDRESS = const(0x6a)
_LSM6DSOX_CHIP_ID = const(0x6C)


_LSM6DSOX_FUNC_CFG_ACCESS = const(0x1)
_LSM6DSOX_PIN_CTRL = const(0x2)
_LSM6DSOX_UI_INT_OIS = const(0x6F)
_LSM6DSOX_WHOAMI = const(0xF)
_LSM6DSOX_CTRL1_XL = const(0x10)
_LSM6DSOX_CTRL2_G = const(0x11)
_LSM6DSOX_CTRL3_C = const(0x12)
_LSM6DSOX_CTRL_5_C = const(0x14)
_LSM6DSOX_MASTER_CONFIG = const(0x14)
_LSM6DSOX_CTRL9_XL = const(0x18)
_LSM6DSOX_OUT_TEMP_L = const(0x20)
_LSM6DSOX_OUT_TEMP_H = const(0x21)
_LSM6DSOX_OUTX_L_G = const(0x22)
_LSM6DSOX_OUTX_H_G = const(0x23)
_LSM6DSOX_OUTY_L_G = const(0x24)
_LSM6DSOX_OUTY_H_G = const(0x25)
_LSM6DSOX_OUTZ_L_G = const(0x26)
_LSM6DSOX_OUTZ_H_G = const(0x27)
_LSM6DSOX_OUTX_L_A = const(0x28)
_LSM6DSOX_OUTX_H_A = const(0x29)
_LSM6DSOX_OUTY_L_A = const(0x2A)
_LSM6DSOX_OUTY_H_A = const(0x2B)
_LSM6DSOX_OUTZ_L_A = const(0x2C)
_LSM6DSOX_OUTZ_H_A = const(0x2D)

_MILLI_G_TO_ACCEL           = 0.00980665

class CV:
    """struct helper"""
    @classmethod
    def _def_value(cls, attr, value, string, lsb):
        setattr(cls, attr, value)
        if not hasattr(cls, 'name'):
            cls.string = {}
        cls.string[value] = string
        if not hasattr(cls, 'lsb'):
            cls.lsb = {}
        cls.lsb[value] = lsb
        if not hasattr(cls, '_valid'):
            cls._valid = []
        cls._valid.append(value)

    @classmethod
    def is_valid(cls, value):
        return value in cls._valid


class AccelRange(CV):
    """Options for `accelerometer_range`"""
    pass

AccelRange._def_value('RANGE_2G', 0, "2G", 0.061)
AccelRange._def_value('RANGE_16G', 1, "16G", 0.488)
AccelRange._def_value('RANGE_4G', 2, "4G", 0.122)
AccelRange._def_value('RANGE_8G', 3, "8G", 0.244)

class GyroRange:
    """Options for `gyro_data_range`"""
    RANGE_250_DPS = const(0)
    RANGE_500_DPS = const(1)
    RANGE_1000_DPS = const(2)
    RANGE_2000_DPS = const(3)
# 1011 1.6 Hz (low power only) 12.5 Hz (high performance)

class Rate:
    """Options for `data_rate`"""
    RATE_SHUTDOWN = const(0)
    RATE_12_5_HZ = const(0b0001)
    RATE_26_HZ = const(0b0010)
    RATE_52_HZ = const(0b0011)
    RATE_104_HZ = const(0b0100)
    RATE_208_HZ = const(0b0101)
    RATE_416_HZ = const(0b0110)
    RATE_833_HZ = const(0b0111)
    RATE_1_66K_HZ = const(0b1000)
    RATE_3_33K_HZ = const(0b1001)
    RATE_6_66K_HZ = const(0b1010)

    RATE_1_6_HZ = const(0b1011) # Accelerometer only, 1.6 Hz low power 12.5 Hz (high performance)



class LSM6DSOX:
    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the LSM6DSOX is connected to.
        :param address: The I2C slave address of the sensor

    """

#ROUnaryStructs:
    _chip_id = ROUnaryStruct(_LSM6DSOX_WHOAMI, "<b")
    _temperature = ROUnaryStruct(_LSM6DSOX_OUT_TEMP_L, "<h")

#RWBits:
    _ois_ctrl_from_ui = RWBit(_LSM6DSOX_FUNC_CFG_ACCESS, 0)
    _shub_reg_access = RWBit(_LSM6DSOX_FUNC_CFG_ACCESS, 6)
    _func_cfg_access = RWBit(_LSM6DSOX_FUNC_CFG_ACCESS, 7)
    _sdo_pu_en = RWBit(_LSM6DSOX_PIN_CTRL, 6)
    _ois_pu_dis = RWBit(_LSM6DSOX_PIN_CTRL, 7)
    _spi2_read_en = RWBit(_LSM6DSOX_UI_INT_OIS, 3)
    _den_lh_ois = RWBit(_LSM6DSOX_UI_INT_OIS, 5)
    _lvl2_ois = RWBit(_LSM6DSOX_UI_INT_OIS, 6)
    _int2_drdy_ois = RWBit(_LSM6DSOX_UI_INT_OIS, 7)
    _lpf_xl = RWBit(_LSM6DSOX_CTRL1_XL, 1)
    
    _accel_range = RWBits(2, _LSM6DSOX_CTRL1_XL, 2)
    _accel_data_rate = RWBits(4, _LSM6DSOX_CTRL1_XL, 4)
    
    _gyro_data_rate = RWBits(4, _LSM6DSOX_CTRL2_G, 4)
    _gyro_range = RWBits(2, _LSM6DSOX_CTRL2_G, 2)

    _sw_reset = RWBit(_LSM6DSOX_CTRL3_C, 0)
    _if_inc = RWBit(_LSM6DSOX_CTRL3_C, 2)
    _sim = RWBit(_LSM6DSOX_CTRL3_C, 3)
    _pp_od = RWBit(_LSM6DSOX_CTRL3_C, 4)
    _h_lactive = RWBit(_LSM6DSOX_CTRL3_C, 5)
    _bdu = RWBit(_LSM6DSOX_CTRL3_C, 6)
    _boot = RWBit(_LSM6DSOX_CTRL3_C, 7)
    _st_xl = RWBits(2, _LSM6DSOX_CTRL_5_C, 0)
    _st_g = RWBits(2, _LSM6DSOX_CTRL_5_C, 2)
    _rounding_status = RWBit(_LSM6DSOX_CTRL_5_C, 4)
    _rounding = RWBits(2, _LSM6DSOX_CTRL_5_C, 5)
    _xl_ulp_en = RWBit(_LSM6DSOX_CTRL_5_C, 7)
    _aux_sens_on = RWBits(2, _LSM6DSOX_MASTER_CONFIG, 0)
    _master_on = RWBit(_LSM6DSOX_MASTER_CONFIG, 2)
    _shub_pu_en = RWBit(_LSM6DSOX_MASTER_CONFIG, 3)
    _pass_through_mode = RWBit(_LSM6DSOX_MASTER_CONFIG, 4)
    _start_config = RWBit(_LSM6DSOX_MASTER_CONFIG, 5)
    _write_once = RWBit(_LSM6DSOX_MASTER_CONFIG, 6)
    _rst_master_regs = RWBit(_LSM6DSOX_MASTER_CONFIG, 7)
    _i3c_disable = RWBit(_LSM6DSOX_CTRL9_XL, 1)
    _den_lh = RWBit(_LSM6DSOX_CTRL9_XL, 2)
    _den_xl_en = RWBit(_LSM6DSOX_CTRL9_XL, 3)
    _den_xl_g = RWBit(_LSM6DSOX_CTRL9_XL, 4)
    _den_z = RWBit(_LSM6DSOX_CTRL9_XL, 5)
    _den_y = RWBit(_LSM6DSOX_CTRL9_XL, 6)
    _den_x = RWBit(_LSM6DSOX_CTRL9_XL, 7)


    _raw_temp = ROUnaryStruct(_LSM6DSOX_OUT_TEMP_L, "<h")

    _raw_accel_data = Struct(_LSM6DSOX_OUTX_L_A, "<hhh")
    _raw_gyro_data = Struct(_LSM6DSOX_OUTX_L_G, "<hhh")

    _gyro_range_lsb = {
        GyroRange.RANGE_250_DPS : 8.75,
        GyroRange.RANGE_500_DPS : 17.50,
        GyroRange.RANGE_1000_DPS : 35.0,
        GyroRange.RANGE_2000_DPS :70
    }

    def __init__(self, i2c_bus, address=_LSM6DSOX_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._chip_id != _LSM6DSOX_CHIP_ID:
            raise RuntimeError("Failed to find LSM6DSOX - check your wiring!")
        self.reset()

        self._bdu = True
        self._accel_data_rate = 3
        self._gyro_data_rate = 3
        self._accel_range = AccelRange.RANGE_4G
        self._cached_accel_range = self._accel_range
        self._gyro_range = GyroRange.RANGE_250_DPS
        self._cached_gyro_range = self._gyro_range
        self._if_inc = True


    def reset(self):
        self._sw_reset = True
        while self._sw_reset:
            sleep(0.001)
        self._boot = True
        while self._boot:
            sleep(0.001)
        
    @property
    def acceleration(self):
        """Acceleration!"""
        raw_accel_data = self._raw_accel_data
        x = self._scale_xl_data(raw_accel_data[0])
        y = self._scale_xl_data(raw_accel_data[1])
        z = self._scale_xl_data(raw_accel_data[2])

        return(x, y, z)

    @property
    def gyro(self):
        """ME GRYO, ME FLY PLANE"""
        raw_gyro_data = self._raw_gyro_data
        x = self._scale_gyro_data(raw_gyro_data[0])
        y = self._scale_gyro_data(raw_gyro_data[1])
        z = self._scale_gyro_data(raw_gyro_data[2])

        return (x, y, z)

    def _scale_xl_data(self, raw_measurement):
        return raw_measurement * AccelRange.lsb[self._cached_accel_range] * _MILLI_G_TO_ACCEL

    def _scale_gyro_data(self, raw_measurement):
        return raw_measurement * self._gyro_range_lsb[self._cached_gyro_range] / 1000

    @property
    def accelerometer_range(self):
        """Adjusts the range of values that the sensor can measure, from +- 2G to +-16G
        Note that larger ranges will be less accurate. Must be an `AccelRange`"""
        return self._cached_accel_range

    @accelerometer_range.setter
    def accelerometer_range(self, value): #pylint: disable=no-member
        if not AccelRange.is_valid(value):
            raise AttributeError("range must be an `AccelRange`")
        self._accel_range = value
        self._cached_accel_range = value

    @property
    def gyro_range(self):
        """Adjusts the range of values that the sensor can measure, from +- 2G to +-16G
        Note that larger ranges will be less accurate. Must be a `Range`"""
        return self._cached_gyro_range

    @gyro_range.setter
    def gyro_range(self, value):
        if not value in [GyroRange.RANGE_250_DPS, GyroRange.RANGE_500_DPS,
            GyroRange.RANGE_1000_DPS, GyroRange.RANGE_2000_DPS
            ]:
            raise AttributeError("range must be a `Range`")
        self._gyro_range = value
        self._cached_gyro_range = value
        sleep(.2) #

    @property
    def data_rate(self):
        """Select the rate at which the sensor takes measurements. Must be a `Rate`"""
        return self._accel_data_rate

    @data_rate.setter
    def data_rate(self, value):
    
        if value not in [Rate.RATE_SHUTDOWN, Rate.RATE_12_5_HZ, Rate.RATE_26_HZ, Rate.RATE_52_HZ,
            Rate.RATE_104_HZ, Rate.RATE_208_HZ, Rate.RATE_416_HZ, Rate.RATE_833_HZ,
            Rate.RATE_1_66K_HZ, Rate.RATE_3_33K_HZ, Rate.RATE_6_66K_HZ, Rate.RATE_1_6_HZ
        ]:
            raise AttributeError("data_rate must be a `Rate`")

        self._accel_data_rate = value

    @property
    def gyro_accel_data_rate(self):
        """Select the rate at which the sensor takes measurements. Must be a `Rate`"""
        return self._gyro_accel_data_rate

    @gyro_accel_data_rate.setter
    def gyro_accel_data_rate(self, value):
        if value not in [Rate.RATE_SHUTDOWN, Rate.RATE_12_5_HZ, Rate.RATE_26_HZ, Rate.RATE_52_HZ,
            Rate.RATE_104_HZ, Rate.RATE_208_HZ, Rate.RATE_416_HZ, Rate.RATE_833_HZ,
            Rate.RATE_1_66K_HZ, Rate.RATE_3_33K_HZ, Rate.RATE_6_66K_HZ
        ]:
            raise AttributeError("gyro_accel_data_rate must be a `Rate`")

        self._gyro_accel_data_rate = value

