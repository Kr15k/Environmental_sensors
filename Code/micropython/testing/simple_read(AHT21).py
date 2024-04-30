import time, machine
import aht

# Example SCL pin and SDA pin for WEMOS D1 mini Lite
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
sensor = aht.AHT2x(i2c, crc=True)

# To print one of measures:
while True:
    if sensor.is_ready:
        print("Humidity: {:.2f}".format(sensor.humidity))
        print("Temperature: {:.2f}".format(sensor.temperature))
        time.sleep(1)