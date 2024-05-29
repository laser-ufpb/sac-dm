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

conn = aiohttp.TCPConnector(limit=200)

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
	print("preparing to post data")
	async with aiohttp.ClientSession(connector=conn) as session:
		post_task=[]
		async for reading in make_readings(sbuffer):
			post_task.append(send_post(session, url, reading))
		await asyncio.gather(*post_task)

async def send_post(session, url, reading):
	reading_split = reading.split(";")
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
#url = 'http://150.164.167.12:8100/accelerometer/'

online = False

ser = serial.Serial("/dev/ttyS0", 115200)
ser.reset_input_buffer()
sensor_buffer = []

log = open("log.txt", "a")


############################ MAIN CODE #################################

esp_serial = str(ser.readline())
	
while True:
		
	esp_serial = str(ser.readline())
	sensor_buffer.append(esp_serial[2:][:-5] + ';'+ str(time.time()))
	
	if len(sensor_buffer) %10000 == 0:
		print(sensor_buffer[-1])
		print(len(sensor_buffer))
		
	if len(sensor_buffer) >= 50000:
		print(len(sensor_buffer))
		print(sensor_buffer[0])

		if(online):
			loop = asyncio.get_event_loop()
			try:
				loop.run_until_complete(send_http(sensor_buffer))
			finally:
				loop.close()
			print("all data posted")
			sensor_buffer.clear()
			#asyncio.run(send_http(sensor_buffer))
					
		else:
			print("saving in file")
			
			for data in sensor_buffer:
				log.write(data)
				log.write("\n")
			print("saved")
			sensor_buffer.clear()
		break;
				


