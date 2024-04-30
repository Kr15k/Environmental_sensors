# check what i2c addresses are to be found on the chosen sda, scl
import machine
i2c = machine.I2C(0,
                  scl=machine.Pin(17),
                  sda=machine.Pin(16),
                  freq=400000)
print(i2c.scan())