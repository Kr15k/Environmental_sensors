# importing libraries and modules
import requests

# https://how2electronics.com/send-sensor-data-to-thingspeak-with-raspberry-pi-pico-w/

HTTP_HEADERS = {'Content-Type': 'application/json'}

THINGSPEAK_WRITE_API_KEY = 'insert_api_key_here' # Use your own api key!!!
THINGSPEAK_WRITE_URL = f'http://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}'

# function for sending data to thingspeak using api key
def thingspeak_publish_data(data):
    payload = {
        'field1' : data["bme"]["temperature"],
        'field2' : data["bme"]["humidity"],
        'field3' : data["bme"]["pressure"],
        'field4' : data["ens"]["tvoc"],
        'field5' : data["ens"]["eco2"],
        'field6' : data["aht"]["temperature"],
        'field7' : data["aht"]["humidity"],
        }
    print(payload)
    r = requests.post(THINGSPEAK_WRITE_URL, json = payload, headers = HTTP_HEADERS)
    return r

# runs if called from main
if __name__ == '__main__':
    from wlan import connect
    sta_if = connect()
    data = dict(
        bme = dict(temperature=0, humidity=0, pressure=0),
        ens = dict(tvoc=0, eco2=0, rating=''),
        aht = dict(temperature=0, humidity=0),
        )
    # publishes data dictionary
    r = thingspeak_publish_data(data)
    print(r.status_code)
    print(r.text)
