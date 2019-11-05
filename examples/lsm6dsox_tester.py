import time
import board
import busio
import adafruit_lsm6dsox

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)

print("Starting test")
# most of this info is from the "Internal pin status" table
# on page 42 of https://www.st.com/resource/en/datasheet/lsm6dsox.pdf

# SETUP:
# VIN - 5V
# GND - GND
# 3V0 - A0
# SDA - A4
# SCL - A5
# SDO/DO, CS, INT1 INT2, SDO_AUX, OCS_AUX, SCX. SDX to digital IO

#VIN/VCC - You'll know pretty quick if it's not working 
# 3Vo - test with A0

# GND see VIN
# SDA \
# SCL _\ Pull ups tested via ADC, function by usage

#SDO Default: input without pull-up.
sox._sdo_pu_en = True # enable pull-up
time.sleep(0.010)

#CS_5V  - LOW will disable I2C, puts in SPI mode

#INT1  - HIGH Will disable I2C , puts in I3C 

#INT2 - Default: output forced to ground
sox._h_lactive = True # switch to hi-z 
time.sleep(0.010)

# SDO_AUX Default: input with pull-up.
# OCS_AUX Default: input with pull-up.

sox._ois_pu_dis = True # disable pull-up
time.sleep(0.010)

# SCX \
# SDX _\ Turn on i2c master pullups 
# enable i2c master register access
# needed because the next register uses a duplicate address
sox._shub_reg_access = True
time.sleep(0.010)
# enable pull ups
sox._shub_pu_en = True
time.sleep(0.010)
# disable i2c master register access
sox._shub_reg_access = False
time.sleep(0.010)

time.sleep(0.5) # hang around for a bit

print("test done")