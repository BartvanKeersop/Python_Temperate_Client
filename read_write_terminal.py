import os
import glob
import time
import datetime
import web_component 

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0000082a2680/w1_slave'

def temp_raw():

	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

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
			json_data = web_component.jsonify(dt, temp_c)
			web_component.post_data(json_data)

while True:
	print(read_temp())
	time.sleep(1)

