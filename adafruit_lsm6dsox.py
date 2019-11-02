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
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VEML7700.git"


_LSM6DS0X_DEFAULT_ADDRESS = const(0x6a)
_LSM6DS0X_CHIP_ID = const(0x6C)


_LSM6DS0X_FUNC_CFG_ACCESS = const(0X1)
_LSM6DS0X_PIN_CTRL = const(0X2)
_LSM6DS0X_UI_INT_OIS = const(0X6F)
_LSM6DS0X_WHOAMI = const(0XF)
_LSM6DS0X_CTRL1_XL = const(0X10)
_LSM6DS0X_CTRL3_C = const(0X12)
_LSM6DS0X_CTRL_5_C = const(0X14)
_LSM6DS0X_MASTER_CONFIG = const(0X14)
_LSM6DS0X_CTRL9_XL = const(0X18)
_LSM6DS0X_OUT_TEMP_L = const(0X20)


class LSM6DSOX:
    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the LSM6DSOX is connected to.
        :param address: The I2C slave address of the sensor

    """

#ROUnaryStructs:
    _chip_id = ROUnaryStruct(_LSM6DS0X_WHOAMI, ">b")
    _temperature = ROUnaryStruct(_LSM6DS0X_OUT_TEMP_L, "<h")

#RWBits:
    _ois_ctrl_from_ui = RWBit(_LSM6DS0X_FUNC_CFG_ACCESS, 0)
    _shub_reg_access = RWBit(_LSM6DS0X_FUNC_CFG_ACCESS, 6)
    _func_cfg_access = RWBit(_LSM6DS0X_FUNC_CFG_ACCESS, 7)
    _sdo_pu_en = RWBit(_LSM6DS0X_PIN_CTRL, 6)
    _ois_pu_dis = RWBit(_LSM6DS0X_PIN_CTRL, 7)
    _spi2_read_en = RWBit(_LSM6DS0X_UI_INT_OIS, 3)
    _den_lh_ois = RWBit(_LSM6DS0X_UI_INT_OIS, 5)
    _lvl2_ois = RWBit(_LSM6DS0X_UI_INT_OIS, 6)
    _int2_drdy_ois = RWBit(_LSM6DS0X_UI_INT_OIS, 7)
    _lpf_xl = RWBit(_LSM6DS0X_CTRL1_XL, 1)
    _fs_xl = RWBits(2, _LSM6DS0X_CTRL1_XL, 2)
    _odr_xl = RWBits(4, _LSM6DS0X_CTRL1_XL, 4)
    _sw_reset = RWBit(_LSM6DS0X_CTRL3_C, 0)
    _if_inc = RWBit(_LSM6DS0X_CTRL3_C, 2)
    _sim = RWBit(_LSM6DS0X_CTRL3_C, 3)
    _pp_od = RWBit(_LSM6DS0X_CTRL3_C, 4)
    _h_lactive = RWBit(_LSM6DS0X_CTRL3_C, 5)
    _bdu = RWBit(_LSM6DS0X_CTRL3_C, 6)
    _boot = RWBit(_LSM6DS0X_CTRL3_C, 7)
    _st_xl = RWBits(2, _LSM6DS0X_CTRL_5_C, 0)
    _st_g = RWBits(2, _LSM6DS0X_CTRL_5_C, 2)
    _rounding_status = RWBit(_LSM6DS0X_CTRL_5_C, 4)
    _rounding = RWBits(2, _LSM6DS0X_CTRL_5_C, 5)
    _xl_ulp_en = RWBit(_LSM6DS0X_CTRL_5_C, 7)
    _aux_sens_on = RWBits(2, _LSM6DS0X_MASTER_CONFIG, 0)
    _master_on = RWBit(_LSM6DS0X_MASTER_CONFIG, 2)
    _shub_pu_en = RWBit(_LSM6DS0X_MASTER_CONFIG, 3)
    _pass_through_mode = RWBit(_LSM6DS0X_MASTER_CONFIG, 4)
    _start_config = RWBit(_LSM6DS0X_MASTER_CONFIG, 5)
    _write_once = RWBit(_LSM6DS0X_MASTER_CONFIG, 6)
    _rst_master_regs = RWBit(_LSM6DS0X_MASTER_CONFIG, 7)
    _i3c_disable = RWBit(_LSM6DS0X_CTRL9_XL, 1)
    _den_lh = RWBit(_LSM6DS0X_CTRL9_XL, 2)
    _den_xl_en = RWBit(_LSM6DS0X_CTRL9_XL, 3)
    _den_xl_g = RWBit(_LSM6DS0X_CTRL9_XL, 4)
    _den_z = RWBit(_LSM6DS0X_CTRL9_XL, 5)
    _den_y = RWBit(_LSM6DS0X_CTRL9_XL, 6)
    _den_x = RWBit(_LSM6DS0X_CTRL9_XL, 7)
    def __init__(self, i2c_bus, address=_LSM6DS0X_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._chip_id != _LSM6DS0X_CHIP_ID:
            raise RuntimeError("Failed to find LSM6DSOX - check your wiring!")
        self.reset()

    def reset(self):
        self._sw_reset = True
        while self._sw_reset:
            sleep(0.001)
        self._boot = True
        while self._boot:
            sleep(0.001)
        
