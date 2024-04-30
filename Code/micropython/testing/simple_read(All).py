# Read air quality metrics from the PiicoDev Air Quality Sensor ENS160
# Shows three metrics: AQI, TVOC and eCO2

from PiicoDev_ENS160 import PiicoDev_ENS160 # import the device driver
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_Unified import sleep_ms       # a cross-platform sleep function
from machine import Pin
import time, machine
import aht

sensor_ens = PiicoDev_ENS160(bus=0, scl=Pin(17), sda=Pin(16))   # Initialise the ENS160 module
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
sensor_aht = aht.AHT2x(i2c)
sensor_bme = PiicoDev_BME280(bus=0, sda=Pin(16), scl=Pin(17), address=0x76)

while True:
    tempC, presPa, humRH = sensor_bme.values() # read all data from bme
    pres_hPa = presPa / 100 # convert Pascals to hPa (mbar)
    
    # Read from the sensor
    aqi = sensor_ens.aqi
    tvoc = sensor_ens.tvoc
    eco2 = sensor_ens.eco2
    
    # Print air quality metrics
    if sensor_aht.is_ready:
        print('1ENS   AQI: ' + str(aqi.value) + ' [' + str(aqi.rating) +']')
        print('1ENS   TVOC: ' + str(tvoc) + ' ppb')
        print('1ENS   eCO2: ' + str(eco2.value) + ' ppm [' + str(eco2.rating) +']')
        print('1ENS Status: ' + sensor_ens.operation)
        print('2AHT   Humidity: {:.2f}'.format(sensor_aht.humidity))
        print('2AHT   Temperature: {:.2f}'.format(sensor_aht.temperature))
        print('3BME   Humidity: ' + str(humRH)+" %RH")
        print('3BME   Temperature: ' + str(tempC)+" °C")
        print('3BME   Pressure: ' + str(pres_hPa)+" hPa")
        print('--------------------------------')
        sleep_ms(1000)