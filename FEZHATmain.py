''''''
import ADS7830
import RPi.GPIO as GPIO
import sys
import json
import logging
from datetime import date
import datetime
import time
from tcpclient2  import transmit
import smbus
from pytz import timezone
# Define sensor channels
light_channel = 5
temperature_channel=4

class FEZHATnew():
    AIN1 = 1
    AIN2 = 2
    AIN3 = 3
    AIN6 = 6
    AIN7 = 7
    GIO26 = 26
    GIO16 = 16
    # onbord switch
    SW_DIO18 = 18
    SW_DIO22 = 22
    # onboard LED
    LED = 24
    def __init__(self):
        self._ads = ADS7830.ADS7830(1, 0x48)
        GPIO.setwarnings(False)# To disable warnings
        GPIO.setmode(GPIO.BCM)# Use Broadcom GPIO pin numbering
        GPIO.setup(self.LED, GPIO.OUT)# To setup GPIO pin 24 to turn the pin off and on
        GPIO.setup(self.SW_DIO18, GPIO.IN)
        GPIO.setup(self.SW_DIO22, GPIO.IN)

    def get_light(self):
        '''To get the Light Dependent Resistor value in kΩ'''
        ldr_value =  self._ads.read(5) / 255.0 # read adc channel 5
        return ldr_value

    def get_temperature(self):
        '''To get the Temperature value in centigrade '''
        gettemp =  (((3300 / 255) * self._ads.read(4)) - 400) / 19.5 # read adc channel 4
        return gettemp
            
    def led_on(self):
        GPIO.output(self.LED, GPIO.HIGH)# TO turn on the GPIO pin 24 on(led on)

    def led_off(self):
        GPIO.output(self.LED, GPIO.LOW)# To turn the GPIO pin24 off while power is not supplying by the pin

    def tempMonitor(self, gettemp, ldr_value):
        utc = timezone('UTC')
        ts = datetime.datetime.now(utc)
        #sensor1 = "{" + "\"pos\":\"A1\"," + "\"deviceid\":\"humiditysensor1\"," + "\"sensor\":\"Temperature\"," + "\"value\":" + "\"" + str(result.temperature) + "\"" + "}"

        # data is in json string


        sensor1="{"+"\"pos\":\"A1\","+"\"deviceid\":\"lightsensor1\","+"\"sensor\":\"light\","+ "\"value\":"+"\""+str(ldr_value)+"\"" +"}"
        sensor2="{"+"\"pos\":\"A1\","+"\"deviceid\":\"temperaturesensor1\","+"\"sensor\":\"temperature\","+"\"value\":"+"\""+ str(gettemp)+"\""+"}"
        # To decode the json string
        jsensor2 = json.loads(sensor2)
        jsensor1 = json.loads(sensor1)
        message1 = "~hydroponics~" + str(ts) + "~lightsensor1~"+ json.dumps(jsensor1) + "\r\n"
        message2 = "~hydroponics~" + str(ts) + "~temperaturesensor1~" + json.dumps(jsensor2) + "\r\n"
        # To send the data on TCPserver
        transmit(message1)
        transmit(message2)
        time.sleep(2)# wait 2 before repeating loop seconds
        
if __name__ == "__main__":
    fh = FEZHATnew()
    while True:
        fh.tempMonitor(fh.get_temperature(), fh.get_light())
        fh.led_on()

        
            
  

    