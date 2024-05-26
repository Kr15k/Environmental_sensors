# importing libraries and modules
from time import sleep
import json
from wlan import connect
import uasyncio
from nanoweb import Nanoweb
import urequests
import gc

import sensors
from html_functions import naw_write_http_header, render_template
#from leds import blink
#import buttons
from thingspeak import thingspeak_publish_data
from machine import WDT
import button

sta_if = connect() # connects to WiFi

naw = Nanoweb() # makes a instance of nanoweb

# defines the data dictionary used to store sensor readings
data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0, rating=''),
    aht = dict(temperature=0, humidity=0),
    )
#inputs = dict(button_1=False)

# posts sensors data to nanoweb page
@naw.route("/")
def index(request):
    naw_write_http_header(request)
    html = render_template(
        'index.html',
        temperature_bme=str(data['bme']['temperature']),
        humidity_bme=str(data['bme']['humidity']),
        pressure=str(data['bme']['pressure']),        
        tVOC=str(data['ens']['tvoc']),
        eCO2=str(data['ens']['eco2']),
        temperature_aht=str(data['aht']['temperature']),
        humidity_aht=str(data['aht']['humidity']),
        )
    await request.write(html)

# displays data as api if added "/api/data" after ip address
@naw.route("/api/data")
def api_data(request):
    naw_write_http_header(request, content_type='application/json')
    await request.write(json.dumps(data))

# async function sending data to thingspeak and garbage collector for safety
async def control_loop():
    while True:
        thingspeak_publish_data(data)
        gc.collect()
        await uasyncio.sleep(60*10)

# async function with a watchdog timer so if something goes wrong it reboots the code
async def wdt_loop():
    wdt = WDT(timeout=8000)
    while True:
        wdt.feed()
        await uasyncio.sleep_ms(1000)

# loops the earlier created async functions
loop = uasyncio.get_event_loop()
loop.create_task(sensors.collect_sensors_data(data, False))
#loop.create_task(buttons.wait_for_buttons(inputs))
loop.create_task(button.air_quality_light(data))
loop.create_task(button.button_loop(data))
loop.create_task(naw.run())
loop.create_task(control_loop())
loop.create_task(wdt_loop())

loop.run_forever()
