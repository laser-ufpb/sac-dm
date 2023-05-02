import requests
import RPi.GPIO as GPIO
import time
import serial
import datetime
from threading import Thread
from threading import Lock

def check_connection():	
	check = requests.get('https://google.com/')
	if(check.status_code):
		return True
	else:
		return False
	
def write_log(data, lock):
	for reading in data:
		with lock:
			log = open("log.txt","a")
			log.write(reading)
			log.write("\n")
			log.close()
		
def write_temp(data, lock):
	for reading in data:
		with lock:
			log = open("temp.txt","a")
			log.write(reading)
			log.write("\n")
			log.close()
	
#def read_temp_send():
	
log_lock = Lock()
temp_lock = Lock()

ser = serial.Serial("/dev/ttyS0", 115200)
url = 'https://enmpf6xid68v.x.pipedream.net/'
sensor_buffer = []




while 1:
	
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + (datetime.datetime.now().strftime(",%d/%b/%Y %H:%M:%S")))
	if len(sensor_buffer) == 10:
		t_log = Thread(target=write_log, args=(sensor_buffer, log_lock,))
		t_log.start()
		connected = check_connection()
		
		if(connected):
			for reading in sensor_buffer:
				print(reading)
				buffer_split = reading.split(",")
				x = requests.post(url, json={'device_code': '01', "ACx": buffer_split[0],"ACy": buffer_split[1],"ACz": buffer_split[2], "time": buffer_split[3]})
			sensor_buffer.clear()
		else:
			t_temp = Thread(target=write_temp, args=(sensor_buffer, temp_lock))
			t_temp.start()
			sensor_buffer.clear()
				
