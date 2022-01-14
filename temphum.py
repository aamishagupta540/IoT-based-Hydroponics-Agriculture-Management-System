import RPi.GPIO as GPIO #import GPIO library
import dht11
import time
import datetime
from tcpclient2 import transmit
import os
import json
from pytz import timezone
# initialize GPIO
GPIO.setwarnings(False)# To disable warnings
GPIO.setmode(GPIO.BCM)# Use Broadcom GPIO pin numbering
GPIO.cleanup()# setup GPIO pin before exiting the program
# read data using pin 14
instance = dht11.DHT11(pin=14)
print("Please enter ctrl-C to quite")
while True:
    result = instance.read()
    if result.is_valid():
        utc = timezone('UTC')
        ts = datetime.datetime.now(utc)
        # data is in json string
        sensor1 = "{" + "\"pos\":\"A1\"," + "\"deviceid\":\"humiditysensor1\"," + "\"sensor\":\"Temperature\"," + "\"value\":" + "\"" + str(result.temperature) + "\"" + "}"
        sensor2 = "{" + "\"pos\":\"A1\"," + "\"deviceid\":\"humiditysensor1\"," + "\"sensor\":\"Humidity\"," + "\"value\":" + "\"" + str(result.humidity) + "\"" + "}"
        # To decode the json string
        jsensor2 = json.loads(sensor2)
        jsensor1 = json.loads(sensor1)
        message1 = "~hydroponics~" + str(ts) + "~humiditysensor1~" + json.dumps(jsensor1) + "\r\n"
        message2 = "~hydroponics~" + str(ts) + "~humiditysensor1~" + json.dumps(jsensor2) + "\r\n"
        # To send the data on TCPserver
        transmit(message1)
        transmit(message2)
    time.sleep(2) # wait for 2 seconds

