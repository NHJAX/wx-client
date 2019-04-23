#!/usr/bin/env python
from SDL_Pi_Thunderboard_AS3935 import  AS3935
import json
import requests
import RPi.GPIO as GPIO
import time
from datetime import datetime
now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
with open('/home/pi/apps/secret-config/api-config.json') as json_data_file:
    data = json.load(json_data_file)
URL = data['BASEURL']
HEADERS = {'NHJax-API-Key':data['NHJax-API-Key']}
Topic = data['LOCATION']
tap = data['Gmail']

GPIO.setmode(GPIO.BCM)

InterruptGPIOpin = 16

sensor = AS3935(address=0x02, bus=1)
def EmailLikeERR():
    print ('You got a error like ERRR')
    import subprocess
    import smtplib
    import socket
    from email.mime.text import MIMEText
    import datetime
    to = 'nhjax-dev@gmail.com'
    gmail_user = 'rpiwxbox@gmail.com'
    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, tap)
    today = datetime.date.today()
    my_ssid = "DoItLikeERR"
    msg = MIMEText(my_ssid)
    msg['Subject'] = 'WX BOX BROKE ON  %s' % today.strftime('%b %d %Y')
    msg['From'] = gmail_user
    msg['To'] = to
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    smtpserver.quit()
    print ('Email sent')

def SendPayload():
    global HEADERS
    global URL
    global payload
    try:
        print ("Sending That Message")
        requests.post(url= URL, headers= HEADERS, data= payload)
    except Exception as e:
        print ("CANNOT SEE THE SERVER!!! the error is ", e)

try:
   sensor.set_indoors(False)
   print ('Sensor Online')
   #raise IOError #uncomment to test err handler
except IOError as e:
   sensor = AS3935(address=0x03, bus=1)
   EmailLikeERR()

sensor.set_indoors(False)
sensor.set_noise_floor(0)
sensor.calibrate(tun_cap=0x09)
sensor.set_min_strikes(1)

count = 0
runcount = 0
def handle_interrupt(channel):
    global count
    global payload
    count = count + 1
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        sensor.raise_noise_floor()
    elif reason == 0x04:
        sensor.set_mask_disturber(True)
    else:
        print ("Whoa did you see that")
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        payload = {"Type": "Lighting", "LightningDetected": "Yes", "Location": Topic, "DistanceKM": distance, "Time": now}
        print (payload)
        SendPayload()

GPIO.setup(InterruptGPIOpin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.add_event_detect(InterruptGPIOpin, GPIO.RISING, callback=handle_interrupt)

print ("Lightning Detection Online @ ", now)
def readLightningStatus():

	distance = sensor.get_distance()
	noise_floor = sensor.get_noise_floor()
	min_strikes = sensor.get_min_strikes()
	indoor = sensor.get_indoors()
	mask_disturber = sensor.get_mask_disturber()
	disp_lco = sensor.get_disp_lco()

while True:
    time.sleep(1.0)
