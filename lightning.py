#!/usr/bin/env python
from SDL_Pi_Thunderboard_AS3935 import  AS3935
import json
import RPi.GPIO as GPIO
import time
from datetime import datetime

with open('/home/pi/apps/secret-config/api-config.json') as json_data_file:
    data = json.load(json_data_file)
print(data)

GPIO.setmode(GPIO.BCM)

InterruptGPIOpin = 16

TOPIC = "jax"

sensor = AS3935(address=0x02, bus=1)


try:

       sensor.set_indoors(False)

       print "Thunder Board present at address 0x02"

except IOError as e:
	sensor = AS3935(address=0x03, bus=1)

        try:

               	sensor.set_indoors(False)

               	print "Thunder Board present at address 0x03"

       	except IOError as e:

        	print "Thunder Board not present"
		exit()

sensor.set_indoors(False)
sensor.set_noise_floor(0)
sensor.calibrate(tun_cap=None)
sensor.set_min_strikes(1)

count = 0
runcount = 0
def handle_interrupt(channel):
    global TOPIC
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
        test = {"Type": "Lighting", "LightningDetected": "Yes", "Location": TOPIC, "DistanceKM": distance, "Time": now}
        print (test)


#GPIO.setup(InterruptGPIOpin, GPIO.IN )
GPIO.setup(InterruptGPIOpin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.add_event_detect(InterruptGPIOpin, GPIO.RISING, callback=handle_interrupt)

print "Waiting for lightning - or at least something that looks like it"

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
