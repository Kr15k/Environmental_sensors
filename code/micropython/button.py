import machine
from machine import Pin, PWM
import sensors
import uasyncio

global lights
lights = True
    
button = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
pins = [11, 12, 13]
freq_num = 10000
pwm0 = PWM(Pin(pins[0])) #set PWM
pwm1 = PWM(Pin(pins[1]))
pwm2 = PWM(Pin(pins[2]))
pwm0.freq(freq_num)
pwm1.freq(freq_num)
pwm2.freq(freq_num)

data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0, rating=''),
    aht = dict(temperature=0, humidity=0),
    )

def setColor(r, g, b):
    pwm0.duty_u16(65535 - r)
    pwm1.duty_u16(65535 - g)
    pwm2.duty_u16(65535 - b)
    
def ratings():
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
    
setColor(0, 0, 0)

async def button_loop():
    global lights
    while True:
        if button.value():
            if lights == False:
                lights = True
                print("lights = True")
                await uasyncio.sleep_ms(1000)
            elif lights == True:
                lights = False
                print("lights = False")
                await uasyncio.sleep_ms(1000)
            print(data['ens']['rating'])
        await uasyncio.sleep_ms(100)

async def air_quality_light():
    global lights
    while True:
        while lights == True:
            ratings()
            #print("light on")
            #print(data['ens']['rating'])
            await uasyncio.sleep_ms(1000)
        if lights == False:
            setColor(0, 0, 0)
            #print("light off")
            #print(data['ens']['rating'])
            await uasyncio.sleep_ms(1000)

def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(sensors.collect_sensors_data(data, False))
    loop.create_task(air_quality_light())
    loop.create_task(button_loop())
    loop.run_forever()

if __name__ == '__main__':
    run()
