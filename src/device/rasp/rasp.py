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
		
async def make_readings(sensor_buffer):
    for r in sensor_buffer:
        yield r		
		
async def send_http(sbuffer):
	url = 'https://enmpf6xid68v.x.pipedream.net/'
	async with aiohttp.ClientSession() as session:
		post_task=[]
		async for reading in make_readings(sbuffer):
			post_task.append(send_post(session, url, reading))
		await asyncio.gather(*post_task)

async def send_post(session, url, reading):
	reading_split = reading.split(",")
	#print(reading_split)
	async with session.post(url, data={
					"device_code":"01",
					"ACx": reading_split[0],
					"ACy": reading_split[1],
					"ACz": reading_split[2],
					"timestamp": reading_split[3]
					}) as response:
						data = await response.text()

	
########################### GLOBAL VAR #################################

url = 'https://enmpf6xid68v.x.pipedream.net/'
#url = 'http://192.168.0.108:8000/accelerometer/'

online = True

ser = serial.Serial("/dev/ttyS0", 115200)
ser.reset_input_buffer()
sensor_buffer = []

############################ MAIN CODE #################################

esp_serial = str(ser.readline())
while True:
	
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ','+ str(time.time()))
	
	if len(sensor_buffer) == 9999:
		break;
		
print(len(sensor_buffer))
print(sensor_buffer[0])

if(online):
	asyncio.run(send_http(sensor_buffer))
				
else:
	
	log = open("log.txt", "a")
	for data in sensor_buffer:
		log.write(data)
		log.write("\n")
			
				
