#!/usr/bin/env python
from SDL_Pi_Thunderboard_AS3935 import  AS3935
import json
import requests
import RPi.GPIO as GPIO
import time
import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
from datetime import datetime
now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
with open('/home/pi/apps/secret-config/api-config.json') as json_data_file:
    data = json.load(json_data_file)
URL = data['BASEURL']
HEADERS = {'NHJax-API-Key':data['NHJax-API-Key']}
Topic = data['LOCATION']

GPIO.setmode(GPIO.BCM)

InterruptGPIOpin = 16

sensor = AS3935(address=0x02, bus=1)

def EmailLikeERR():
    to = 'nhjax-dev@gmail.com'
    gmail_user = 'rpiwxbox@gmail.com'
    gmail_password = 'ZAQ!2wsx'
    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.login(gmail_user, gmail_password)
    today = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
    text = "The box has a problem "
    msg = MIMEText(text)
    msg['Subject'] = Topic, ' WX BOX had a ERR'
    msg['From'] = gmail_user
    msg['To'] = to
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    smtpserver.quit()

try:
    sensor.set_indoors(False)
    raise IOError
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
    count = count + 1
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        sensor.raise_noise_floor()
    elif reason == 0x04:
        sensor.set_mask_disturber(True)
    else:
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        payload = {"Type": "Lighting", "LightningDetected": "Yes", "Location": Topic, "DistanceKM": distance, "Time": now}
        print (payload)
        requests.post(url= URL, headers= HEADERS, data= payload)

GPIO.setup(InterruptGPIOpin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.add_event_detect(InterruptGPIOpin, GPIO.RISING, callback=handle_interrupt)

def readLightningStatus():

	distance = sensor.get_distance()
	noise_floor = sensor.get_noise_floor()
	min_strikes = sensor.get_min_strikes()
	indoor = sensor.get_indoors()
	mask_disturber = sensor.get_mask_disturber()
	disp_lco = sensor.get_disp_lco()

while True:
    time.sleep(1.0)
