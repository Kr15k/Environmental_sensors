from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_Unified import sleep_ms # cross-platform compatible sleep function
from machine import Pin

sensor = PiicoDev_BME280(bus=0, sda=Pin(16), scl=Pin(17), address=0x76) # initialise the sensor

while True:
    tempC, presPa, humRH = sensor.values() # read all data
    pres_hPa = presPa / 100 # convert Pascals to hPa (mbar)
    print(str(tempC)+" °C  " + str(pres_hPa)+" hPa  " + str(humRH)+" %RH")
    sleep_ms(1000)