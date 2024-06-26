# importing libraries and modules
import gc
from time import sleep
from machine import Pin, I2C
import uasyncio
from PiicoDev_BME280 import PiicoDev_BME280 # import bme library
from PiicoDev_ENS160 import PiicoDev_ENS160 # import ens library
from PiicoDev_Unified import sleep_ms       # a cross-platform sleep function
import aht # import aht library

# temperature offset, guess made from other temperature readings (differs from every sensor)
bme_temp_offset = 4
aht_temp_offset = 8

# difining bus, scl & sda pin
bme = PiicoDev_BME280(bus=0, sda=Pin(16), scl=Pin(17), address=0x76)
ens = PiicoDev_ENS160(bus=0, scl=Pin(17), sda=Pin(16))
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
aht_sensor = aht.AHT2x(i2c, crc=False)

# defining arrays for each sensor value, and a string value for the ens rating
readings_bme_temperature = []
readings_bme_humidity = []
readings_bme_pressure = []
readings_ens_tvoc = []
readings_ens_eco2 = []
readings_ens_rating = ''
readings_aht_temperature = []
readings_aht_humidity = []

# async function for reading bme
async def read_bme():
    temperature, pressure, humidity = bme.values() # read all data from bme
    return temperature, humidity, pressure

# async function for reading ens
async def read_ens():
    return ens.tvoc, ens.eco2.value, ens.eco2.rating

# async function for reading aht
async def read_aht():
    if aht_sensor.is_ready:
        temperature = aht_sensor.temperature
        humidity = aht_sensor.humidity  
    return temperature, humidity

def _pop0(l):
    if len(l) >= 60:
        l.pop(0)

# function for finding the median
def _mid(l):
    return sorted(l)[len(l)//2]

# async function updating sensor readings
async def update_sensors_data(data):
    global readings_bme_temperature
    global readings_bme_humidity
    global readings_bme_pressure
    global readings_ens_tvoc
    global readings_ens_eco2
    global readings_ens_rating    
    global readings_aht_temperature
    global readings_aht_humidity

    temperature, humidity, pressure = await read_bme()
    readings_bme_temperature.append(temperature)
    readings_bme_humidity.append(humidity)
    readings_bme_pressure.append(pressure)

    tvoc, eco2, rating = await read_ens()
    readings_ens_tvoc.append(tvoc)
    readings_ens_eco2.append(eco2)
    readings_ens_rating = rating

    temperature, humidity = await read_aht()
    readings_aht_temperature.append(temperature)
    readings_aht_humidity.append(humidity)

    _pop0(readings_bme_temperature)
    _pop0(readings_bme_humidity)
    _pop0(readings_bme_pressure)

    _pop0(readings_ens_tvoc)
    _pop0(readings_ens_eco2)

    _pop0(readings_aht_temperature)
    _pop0(readings_aht_humidity)

    # stores new readings after finding median and applying offsets
    data['bme']['temperature'] = _mid(readings_bme_temperature) - bme_temp_offset
    data['bme']['humidity'] = _mid(readings_bme_humidity)
    data['bme']['pressure'] = _mid(readings_bme_pressure)
    data['ens']['tvoc'] = _mid(readings_ens_tvoc)
    data['ens']['eco2'] = _mid(readings_ens_eco2)
    data['ens']['rating'] = readings_ens_rating
    data['aht']['humidity'] = _mid(readings_aht_humidity)
    data['aht']['temperature'] = _mid(readings_aht_temperature) - aht_temp_offset

async def collect_sensors_data(data, test=False):    
    while True:
        await update_sensors_data(data)
        if test:
            print(data)
        await uasyncio.sleep_ms(5000)

# function to run if ran from main that will loop because of uasyncio
def looping():
    data = dict(
        bme = dict(temperature=0, humidity=0, pressure=0),
        ens = dict(tvoc=0, eco2=0, rating=''),
        aht = dict(temperature=0, humidity=0),
    )
    loop = uasyncio.get_event_loop()
    loop.create_task(collect_sensors_data(data, True))
    loop.run_forever()

# runs if called from main
if __name__ == '__main__':
    looping()
