import urllib.request
import requests
import RPi.GPIO as GPIO
import time
import serial
import json as JSON
from threading import Thread
from threading import Lock

############################ SEND HTTP ################################# 



def check_connection(host='https://google.com/'):	
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False

def sendJSONhttp(data, lock):
	print("prepping json")
	json_obj_array = []
	for r in data:
		split = r.split(";")
		item = {'device_code':'01',
				'ACx': split[0],
				'ACy': split[1],
				'ACz': split[2],
				'timestamp': split[3]}
		json_obj_array.append(item)
		
	json_string = JSON.dumps(json_obj_array)
	with lock:
		response = requests.post(url, data=json_string, headers={"Content-Type":"application/json"})
		print(response.text)

############################ TEXT FILES ################################
		
def write_log(log, data, lock):
	for reading in data:
		with lock:
			log.write(reading)
			log.write("\n")

	
########################### GLOBAL VAR #################################



url = 'https://enmpf6xid68v.x.pipedream.net/'
#url = 'http://150.165.167.12:8100/accelerometer/'

ser = serial.Serial("/dev/ttyS0", 115200)
ser.reset_input_buffer()
sensor_buffer = []

log = open("log.txt", "a")

log_lock = Lock()
http_lock = Lock()


############################ MAIN CODE #################################

esp_serial = str(ser.readline())
	
while True:
		
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ';'+ str(time.time()))
	
	if len(sensor_buffer) %10000 == 0:
		print(sensor_buffer[-1])
		print(len(sensor_buffer))
		
	if len(sensor_buffer) >= 100:
		print(len(sensor_buffer))
		print(sensor_buffer[0])
		
		toSend = sensor_buffer.copy()

		if(check_connection()):
			
			print("online")
			t_http = Thread(target=sendJSONhttp, args=(toSend, http_lock))
			t_http.start()
			sensor_buffer.clear()		
			
					
		else:
			
			print("offline")
			t_log = Thread(target=write_log, args=(log, toSend, log_lock,))
			t_log.start()
			sensor_buffer.clear()
			
		break;
				


