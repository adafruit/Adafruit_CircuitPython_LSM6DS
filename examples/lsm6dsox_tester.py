import time
import board
import busio
import adafruit_lsm6dsox

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6dsox.LSM6DSOX(i2c)

#CS_5V  - LOW will disable I2C, puts in SPI mode
#INT1 #float/internal pulldown= i2c& i3c :: HIGH = I3C only/I2C disabled
    
#SDO _sdo_pu_en
sox._sdo_pu_en = True # toggle SD0
time.sleep(0.010)
#SCX &  #SDX _
#access master registers
sox._shub_reg_access = True
time.sleep(0.010)
# enable pull up
sox._shub_pu_en = True
time.sleep(0.010)
#block master registers
sox._shub_reg_access = False
time.sleep(0.010)

#INT2
sox._h_lactive = True
time.sleep(0.010)
#OCS_AUX& #SDO_AUX
#sox._sim_ois = True
#time.sleep(0.010)

sox._ois_pu_dis = False
time.sleep(0.010)

time.sleep(0.2) # switch polarity of int2