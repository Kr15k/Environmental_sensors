# importing libraries and modules
import machine
from machine import Pin, PWM
import sensors
import uasyncio
import time

# setting pwm led pins, frequency, button pin & lights boolean
button = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
pins = [11, 12, 13]
frq = 10000
pwm0 = PWM(Pin(pins[0])) #set PWM
pwm1 = PWM(Pin(pins[1]))
pwm2 = PWM(Pin(pins[2]))
pwm0.freq(frq)
pwm1.freq(frq)
pwm2.freq(frq)
lights = True

# defining the data dictionary that will be used to contain sensor readings
"""
data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0, rating=''),
    aht = dict(temperature=0, humidity=0),
    )
"""

# function to set color based on r, g & b values
def setColor(r, g, b):
    pwm0.duty_u16(65535 - r)
    pwm1.duty_u16(65535 - g)
    pwm2.duty_u16(65535 - b)

# changes color of the led based on what the air quality is
def ratings(data):
    
    if data['ens']['rating'] == 'excellent':
        setColor(0, 2000, 0)
    elif data['ens']['rating'] == 'good':
        setColor(500, 500, 0)
    elif data['ens']['rating'] == 'fair':
        setColor(2000, 500, 0)
    elif data['ens']['rating'] == 'poor':
        setColor(3000, 300, 0)
    elif data['ens']['rating'] == 'bad':
        setColor(3000, 0, 0)

# async function for cheecking if the button gets pressed
async def button_loop(data):
    global lights
    while True:
        if button.value():
            if lights == False:
                lights = True
                #print("lights = True")
                await uasyncio.sleep_ms(1000)
            elif lights == True:
                lights = False
                #print("lights = False")
                await uasyncio.sleep_ms(1000)
            #print(data['ens']['rating'])
        await uasyncio.sleep_ms(100)

# async function changing light on or off depending on a boolean
async def air_quality_light(data):
    global lights
    while True:
        # turning the light off at 10pm and on at 10am (can still be toggled at all other hours)
        hour = time.localtime()[3]
        if hour == 11:
            lights = False
        elif hour == 10:
            lights = True
            
        if lights == True:
            ratings(data)
            #print("light on")
            #print(data['ens']['rating'])
            await uasyncio.sleep_ms(1000)
        elif lights == False:
            setColor(0, 0, 0)
            #print("light off")
            #print(data['ens']['rating'])
            await uasyncio.sleep_ms(1000)

# function containing the loop for button and light
def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(sensors.collect_sensors_data(data, False))
    loop.create_task(air_quality_light(data))
    loop.create_task(button_loop(data))
    loop.run_forever()

#run()