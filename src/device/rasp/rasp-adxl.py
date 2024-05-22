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
	#print("prepping json")
	json_obj_array = []
	for r in data:
		split = r.split(";")
		try:
			item = {'device_id': 1,
					'label': 'FCT560',
					'ACx': float(split[0]),
					'ACy': float(split[1]),
					'ACz': float(split[2]),
					'timestamp': split[3]}
			json_obj_array.append(item)
		except ValueError:
			continue
	
	json_string = JSON.dumps(json_obj_array)
	with lock:
		print("enviando")
		requests.post(url, data=json_string, headers={"Content-Type":"application/json"})
		print("enviado")


############################ TEXT FILES ################################
		
def write_log(data, lock):
	log = open("log.txt", "a")
	for reading in data:
		with lock:
			log.write(reading + "\n")
	log.close()

#def read_log_send(lock)
#	sendHttp = []
#
#	with lock:
#		log = open("log.txt", "r")
#		lines = log.readlines()
#		log.close()
#		for l in lines:
#			sendHttp.append(l.strip())
#		if(sendJSONhttp(sendHttp, http_lock) == 200):
#			log = open("log.txt", "w")
#			log.close()
#			sendHttp.clear()
	
		
		
	
########################### GLOBAL VAR #################################




#url = 'https://enmpf6xid68v.x.pipedream.net/'
url = 'http://192.168.0.117:8100/accelerometer/'

ser = serial.Serial("/dev/ttyS0", 921600)
ser.reset_input_buffer()
sensor_buffer = []

online = False
log_lock = Lock()
http_lock = Lock()

send_count =0

############################ MAIN CODE #################################

esp_serial = str(ser.readline())
	
while True:
	
	start=time.time()	
	
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ';'+ str(time.time_ns()*1000000))
	
#	if len(sensor_buffer) %1000 == 0:
#		print(sensor_buffer[-1])
#		print(len(sensor_buffer))
		
	if len(sensor_buffer) >= 15000:
		
		print(time.time()-start)
		
		print(len(sensor_buffer))
		print(sensor_buffer[0])
		
		toSend = sensor_buffer.copy()

		if(online):
			
			print("online")
			t_http = Thread(target=sendJSONhttp, args=(toSend, http_lock))
			t_http.start()
			sensor_buffer.clear()		
			send_count=send_count+1

					
		else:
			
			print("offline")
			t_log = Thread(target=write_log, args=(toSend, log_lock,))
			t_log.start()
			sensor_buffer.clear()
			
		#break
		if(send_count==20):
			break


