#!/usr/bin/env python
from SDL_Pi_Thunderboard_AS3935 import  AS3935
import json
import RPi.GPIO as GPIO
import time
import requests
import sys
import os
from datetime import datetime
now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
with open('/home/pi/apps/secret-config/api-config.json') as json_data_file:
    data = json.load(json_data_file)
def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                    relative)
with open('/home/pi/apps/secret-config/certs/publickey.pem') as pk:
    public_key = resource_path(pk)
URL = data['BASEURL']
HEADERS = {'NHJax-API-Key':data['NHJax-API-Key']}
Topic = data['location']
payload = {"Type": "Lighting", "LightningDetected": "No", "Location": Topic, "DistanceKM": "0", "Time": now}

#requests.post(url= URL, headers= HEADERS, data= payload)

#print (URL)
#print (HEADERS)
#print (Topic)

GPIO.setmode(GPIO.BCM)

InterruptGPIOpin = 16

sensor = AS3935(address=0x02, bus=1)


try:

    sensor.set_indoors(False)

    print ("Thunder Board present at address 0x02")

except IOError as e:

    sensor = AS3935(address=0x03, bus=1)

    try:

        sensor.set_indoors(False)

        print ("Thunder Board present at address 0x03")

    except IOError as e:
        print ("Thunder Board not present")
        exit()

sensor.set_indoors(False)
sensor.set_noise_floor(0)
sensor.calibrate(tun_cap=None)
sensor.set_min_strikes(1)

count = 0
runcount = 0
def handle_interrupt(channel):
    global count
    global test
    count = count + 1
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        sensor.raise_noise_floor()
    elif reason == 0x04:
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        payload = {"Type": "Lighting", "LightningDetected": "Yes", "Location": Topic, "DistanceKM": distance, "Time": now}
        requests.post(url= URL, headers= HEADERS, data= payload, verify= public_key)


#GPIO.setup(InterruptGPIOpin, GPIO.IN )
GPIO.setup(InterruptGPIOpin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.add_event_detect(InterruptGPIOpin, GPIO.RISING, callback=handle_interrupt)

print ("Waiting for lightning - or at least something that looks like it")
payload = {"Type": "Lighting", "LightningDetected": "Yes", "Location": Topic, "DistanceKM": "0", "Time": "0"}
requests.post(url= URL, headers= HEADERS, data= payload, verify= public_key)


# def readLightningStatus():

	# distance = sensor.get_distance()
	# noise_floor = sensor.get_noise_floor()
	# min_strikes = sensor.get_min_strikes()
	# indoor = sensor.get_indoors()
	# mask_disturber = sensor.get_mask_disturber()
	# disp_lco = sensor.get_disp_lco()
	# #interrupt = sensor.get_interrupt()
    #
	# print "---------"
	# print "distance=", distance
	# print "noise_floor=", noise_floor
	# print "min_strikes=", min_strikes
	# print "indoor=", indoor
	# print "mask_disturber=", mask_disturber
	# print "disp_lco=", disp_lco
	# print "count=", count
	# #print "interrupt=", interrupt


while True:
    time.sleep(1.0)
    #readLightningStatus()
