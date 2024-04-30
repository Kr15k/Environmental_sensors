# importing libraries and modules
import network
import time

SSID = 'ssid' #use your WiFi's SSID
PASSWORD = 'password' #use your WiFi's password

# funtion for connecting to provided SSID
def connect():
    sta_if = network.WLAN(network.STA_IF)
    # checks if already connected to network
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        c = 0
        # a counter for while its not connected
        while sta_if.isconnected() == False:
            c += 1
            time.sleep(0.2)
            # if connection takes too long, prints "connection failed"
            if c > 50:
                print('Connection failed')
                break
        # if connection takes too long, prints "connection failed"
        if c <= 50:
            print('Connection successful')
    else:
        print('Already connected!')
    print(sta_if.ifconfig())
    return sta_if

# runs if called from main
if __name__ == '__main__':
    sta_if = connect()
    nets = sta_if.scan()
    for n in nets:
        print(n)
