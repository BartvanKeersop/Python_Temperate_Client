# this code reads temperature, and sends it using a POST HTTP request.
# Made by Bart van Keersop, Jim Vercoelen & Luitzen-Jan Beiboer
# OAMK University of applied science 2017, Embedded System Development

import sys
import os
import glob
import time
import datetime
import requests 

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# global variables
global api_url = 'https://requestb.in/1ck7q7q1'
global temp_sensor = '/sys/bus/w1/devices/28-0000082a2680/w1_slave'

# reads and converts the sensor data.
# returns: current time as datetime
# returns: temperature in celcius as string
def read_temp():
	lines = temp_raw()
	while lines[0].strip()[-3] != 'YES':
		time.sleep(0.2)
		lines = temp_raw()
		temp_output = lines[1].find('t=')
		if temp_output != -1:
			temp_string = lines[1].strip()[temp_output+2:]
			temp_c = float(temp_string)/1000.0
			dt = datetime.datetime.now()
            return dt, temp_c

# helper function for read_temp
# reads the raw sensor data
def temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

# posts the measured data to defined url
# arg1: time as datetime
# arg2: measured temperature as string
def post_data(time, temp_c):
    data = jsonify(time, temp_c)
	url = 'https://requestb.in/1ck7q7q1'
	headers = {'accept': 'application/json','content-type': 'application/json'}  
	r = requests.post(url, data = data, headers = headers)

# helper function for post_data
# converts the given parameters to a json format
# arg1: time as datetime
# arg2: measured temperature as string
def jsonify(time, temp_c):
	data = '{\'time\':\'%s\',\'temp\':\'%s\'}' % (time, temp_c)
	return data

# loop to keep the function running
# sends data to api every <argument> seconds
while True:
    post_data(read_temp())
	time.sleep(sys.argv[1])
