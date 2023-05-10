import urllib.request
import requests
import aiohttp
import asyncio
import RPi.GPIO as GPIO
import time
import serial
from threading import Thread
from threading import Lock

############################ SEND HTTP ################################# 


def check_connection(host='https://google.com/'):	
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False
		
#async def make_readings(sensor_buffer):
#    for r in sensor_buffer:
#        yield r		
		
#async def send_http(sbuffer):
#	url = 'https://enmpf6xid68v.x.pipedream.net/'
#	async with aiohttp.ClientSession() as session:
#		post_task=[]
#		#async for reading in sbuffer:
#		async for reading in make_readings(sbuffer):
#			post_task.append(send_post(session, url, reading))
#		await asyncio.gather(*post_task)

#async def send_post(session, url, reading):
#	reading_split = reading.split(",")
#	#print(reading_split)
#	async with session.post(url, data={
#					"device_code":"01",
#					"ACx": reading_split[0],
#					"ACy": reading_split[1],
#					"ACz": reading_split[2],
#					"timestamp": reading_split[3]
#					}) as response:
#						data = await response.text()

url = 'https://enmpf6xid68v.x.pipedream.net/'
def send_http(data,lock):
	buffer_split = reading.split(",")
	x = requests.post(url, json={'device_code': '01',
								"ACx": buffer_split[0],
								"ACy": buffer_split[1],
								"ACz": buffer_split[2], 
								"time": buffer_split[3]})
		
############################ TEXT FILES ################################
		
def write_log(log, data, lock):
	for reading in data:
		with lock:
			log.write(reading)
			log.write("\n")

		
def write_temp(temp, data, lock):
	for reading in data:
		with lock:
			temp.write(reading)
			temp.write("\n")
	
#def read_temp_send():

		
############################ MAIN CODE #################################

log_lock = Lock()
temp_lock = Lock()

ser = serial.Serial("/dev/ttyS0", 115200)
ser.reset_input_buffer()

sensor_buffer = []

log = open("log.txt","a")
temp = open("temp.txt","a")

start = time.time()
esp_serial = str(ser.readline())

while True:
	
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ','+ str(time.time()))
	
	if len(sensor_buffer) >= 1000:
	
		t_log = Thread(target=write_log, args=(log, sensor_buffer, log_lock,))
		t_log.start()
		if(check_connection()):
			x=0
			#asyncio.run(send_http(sensor_buffer))
			#t_http = Thread(target=send_http, args=(sensor_buffer))
			sensor_buffer.clear()
				
		else:
			t_temp = Thread(target=write_temp, args=(temp, sensor_buffer, temp_lock))
			t_temp.start()
			sensor_buffer.clear()
			
	if ((time.time() - start) > 100):
		print("finishing\n")
		print(time.time() - start)
		break
				
