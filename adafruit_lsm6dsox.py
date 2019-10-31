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
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VEML7700.git"


_LSM6DS0X_DEFAULT_ADDRESS = const(0x6a)
_LSM6DS0X_CHIP_ID = const(0x6C)


#Register Consts: 

_LSM6DS0X_WHOAMI = const(0XF)
_LSM6DS0X_OUT_TEMP_L = const(0X20)



class LSM6DSOX:
    """Driver for the LSM6DSOX 6-axis accelerometer and gyroscope.

        :param ~busio.I2C i2c_bus: The I2C bus the MPU6050 is connected to.
        :param address: The I2C slave address of the sensor

    """
#ROUnaryStructs:


    _chip_id = ROUnaryStruct(_LSM6DS0X_WHOAMI, ">b")
    _temperature = ROUnaryStruct(_LSM6DS0X_OUT_TEMP_L, "<h")
    
    def __init__(self, i2c_bus, address=_LSM6DS0X_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._chip_id != _LSM6DS0X_CHIP_ID:
            raise RuntimeError("Failed to find MPU6050 - check your wiring!")
        print("IT'S VERKINK!")
        #self.reset()


# get i2c address
# get register map
# add init code/whoami check
# add reset fn
# test pins:
#VIN/VCC
#3V0
#SCL SDA#
#SDO 
#CS_5V
#INT1, INT2
#SDO_AUX
#OCS_AUX
#SDX
#SCX

