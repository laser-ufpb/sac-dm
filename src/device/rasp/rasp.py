import urllib.request
import requests
import RPi.GPIO as GPIO
import time
import serial
import json as JSON
from threading import Thread
from threading import Lock

############################ SEND HTTP #################################

def convertData(d):
	fdata = float(d)
	converted = ((fdata)*9.80665)/4096
	return round(converted, 2) 



def check_connection(host='https://google.com/'):	
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False

def sendJSONhttp(data, lock):
	#print("prepping json")
	json_obj_array = []
	for r in data:
		split = r.split(";")
		item = {'device_id':'01',
				'ACx': convertData(split[0]),
				'ACy': convertData(split[1]),
				'ACz': convertData(split[2]),
				'timestamp': split[3]}
		json_obj_array.append(item)
		
	json_string = JSON.dumps(json_obj_array)
	with lock:
		response = requests.post(url, data=json_string, headers={"Content-Type":"application/json"})
		print(response.status_code)
		return response.status_code

############################ TEXT FILES ################################
		
def write_log(data, lock):
	log = open("log.txt", "a")
	for reading in data:
		with lock:
			log.write(reading)
			log.write("\n")
	log.close()

def read_log_send(lock)
	sendHttp = []

	with lock:
		log = open("log.txt", "r")
		lines = log.readlines()
		log.close()
		for l in lines:
			sendHttp.append(l.strip())
		if(sendJSONhttp(sendHttp, http_lock) == 200):
			log = open("log.txt", "w")
			log.close()
			sendHttp.clear()
	
		
		
	
########################### GLOBAL VAR #################################



#url = 'https://enmpf6xid68v.x.pipedream.net/'
url = 'http://150.165.167.12:8100/accelerometer/'

ser = serial.Serial("/dev/ttyS0", 115200)
ser.reset_input_buffer()
sensor_buffer = []

disconnected_flag = 0 # 1 if previously disconnected then reconnect to wifi, 0 if not

log_lock = Lock()
http_lock = Lock()


############################ MAIN CODE #################################

esp_serial = str(ser.readline())
	
while True:
	
	start=time.time()	
	
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ';'+ str(time.time_ns()*1000000))
	
	if len(sensor_buffer) %10000 == 0:
		print(sensor_buffer[-1])
		print(len(sensor_buffer))
		
	if len(sensor_buffer) >= 10000:
		
		print(time.time()-start)
		
		print(len(sensor_buffer))
		print(sensor_buffer[0])
		
		toSend = sensor_buffer.copy()

		if(check_connection()):
			
			if(disconnected_flag):
				read_log_send()
			
			print("online")
			t_http = Thread(target=sendJSONhttp, args=(toSend, http_lock))
			t_http.start()
			sensor_buffer.clear()		
			
					
		else:
			
			disconnected_flag = 1
			print("offline")
			t_log = Thread(target=write_log, args=(toSend, log_lock,))
			t_log.start()
			sensor_buffer.clear()
			
		#break;
				


