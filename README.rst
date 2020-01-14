Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-lsm6dsox/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/lsm6dsox/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX/actions
    :alt: Build Status

CircuitPython library for the ST LSM6DSOX 6-axis Accelerometer and Gyro


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-lsm6dsox/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-lsm6dsox

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-lsm6dsox

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-lsm6dsox

Usage Example
=============
.. code-block:: python

    import time
    import board
    import busio
    import adafruit_lsm6ds

    i2c = busio.I2C(board.SCL, board.SDA)

    sox = adafruit_lsm6ds.LSM6DSOX(i2c)

    while True:
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(sox.gyro))
        print("")
        time.sleep(0.5)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
