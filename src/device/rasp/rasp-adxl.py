import urllib.request
import requests
import RPi.GPIO as GPIO
import time
import serial
import json as JSON
import os


import numpy as np
from scipy.signal import find_peaks

#import sys
#import os
#sys.path.append(os.path.abspath("../../sac-dm/"))
#from sacdm import sac_am

from threading import Thread
from threading import Lock

# Calcula SAC-AM (amplitude media dos maximos) utilizando a funcao find_peaks do Python
def sac_am(data, N):
	
	M = len(data)
	size = int(M/N)
	if(M%N):
		size += 1
	sacdm=[0.0] * size
	
	inicio = 0
	fim = N
	for k in range(size):
		peaks, _ = find_peaks(data[inicio:fim])
		v = np.abs(data[peaks])
		s = np.mean(v)
		sacdm[k] = 1.0*s/N
		inicio = fim
		fim = fim + N

	return sacdm

def average_sac(dataset):

	start=0
	end=len(dataset)

	average = np.average(dataset[start:end])

	return average

def deviation_sac(dataset):
	
	start=0
	end=len(dataset)

	standard_deviation = np.std(dataset[start:end])

	return standard_deviation	
	
def get_device_code(interface):
	#endereco mac da rasp e retorna
	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = '00:00:00:00:00:00'
	#print(mac[0:17])
	return mac[0:17]

def compute_mean_dev():
	
	device = requests.get(url+'device_by_code/'+str(get_device_code('wlan0')))
	
	#print(json().dumps(device, indet=4, ensure_ascii=False))
	
	vehicleId = str(device.json()['vehicle_id'])
	
	vehicle = requests.get(url+'sacdm_default?vehicle_id=' + str(device.json()['vehicle_id']))
	
	print(vehicle.json())
	
	
	#checa se encontra media e desvio no servidor
	if vehicle.json() is not None:
		return
	else:
		data=[]
		count=0
		
		while True:
			esp_serial = str(ser.readline())
			data.append(esp_serial[2:][:-5])
			
			if(len(data)%15000 == 0):
				count+=1
				print(count)
				print(esp_serial[2:][:-5])
			
			if(len(data)>= 15000):
				break
		x=[]
		y=[]
		z=[]
		for r in data:
			split = r.split(';')
			if len(split) < 3:
				continue
			try:
				print(r)
				x.append(float(split[0])) #x
				y.append(float(split[1])) #y
				z.append(float(split[2])) #z
			except ValueError or IndexError:
				continue
		
		sac_x = sac_am(np.array(x), 1000)
		sac_y = sac_am(np.array(y), 1000)
		sac_z = sac_am(np.array(z), 1000)
		
		mean_x = average_sac(sac_x)
		deviation_x = deviation_sac(sac_x)
		
		mean_y = average_sac(sac_y)
		deviation_y = deviation_sac(sac_y)
		
		mean_z = average_sac(sac_z)
		deviation_z = deviation_sac(sac_z)
		
		print('X: ',mean_x, ' --- ', deviation_x)
		print('Y: ',mean_y, ' --- ', deviation_y)
		print('Z: ',mean_z, ' --- ', deviation_z)
			
		obj = {
			'vehicle_id': device.json()['vehicle_id'],
			'x_mean': mean_x,
			'x_standard_deviation': deviation_x,
			'y_mean': mean_y,
			'y_standard_deviation': deviation_y,
			'z_mean': mean_z,
			'z_standard_deviation': deviation_z,
			}
		send_json = JSON.dumps(obj)
		response = requests.post(url+'sacdm_default', data=send_json, headers={"Content-Type":"application/json"})
		print(response.status_code)
	
############################ SEND HTTP #################################

def check_connection(host='https://google.com/'):	
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False

def sendJSONhttp(data, lock):
	print("prepping json")
	
	array_mean_test =[]
	
	json_obj_array = []
	x_array=[]
	y_array=[]
	z_array=[]
	for r in data:
		split = r.split(";")
		try:
			x_array.append(float(split[0])) #x
			y_array.append(float(split[1])) #y
			z_array.append(float(split[2])) #z
		except ValueError:
			continue
		except IndexError:
			continue
			
			
	#mean_x = average_sac(np.array(x_array))
	#print("Mean X:", mean_x)
	
	#mean_y = average_sac(np.array(y_array))
	#print("Mean Y:", mean_y)
			
	#mean_z = average_sac(np.array(z_array))
	#print("Mean Z:", mean_z)
	
	sac_array_x = sac_am(np.array(x_array), 1000) ####
	sac_array_y = sac_am(np.array(y_array), 1000)
	sac_array_z = sac_am(np.array(z_array), 1000)
	for i in range(len(sac_array_x)):
		if(sac_array_x[i]):
			item = {'device_id': 1,
					'x_value': sac_array_x[i],
					'y_value': sac_array_y[i],
					'z_value': sac_array_z[i],
					'timestamp': str(time.time_ns()*1000000),
					'label': 'teste 01',
					'vehicle_id': vehicleId
					}
			json_obj_array.append(item)
	#print("Mean: ", average_sac(sac_array_x))
	json_string = JSON.dumps(json_obj_array)
	with lock:
		print("enviando")
		status = requests.post(url + 'sac_dm', data=json_string, headers={"Content-Type":"application/json"})
		print(status.json())

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
#		if(sendJSONhttp(sendHttp, http_lock).status_code == 200):
#			log = open("log.txt", "w")
#			log.close()
#			sendHttp.clear()

##########################

def check_serial_ready():
	while True:
		try:
			ser = serial.Serial("/dev/ttyUSB0", 921600)
			if ser.is_open:
				print("Conexao com a serial estabelecida")
				return ser
		except serial.SerialException:
			print("Aguardando a conexao serial, tentando novamente em 3 segundos")
			time.sleep(3)
			
def adxl_transmiter(device_status_stop, is_online):
	iterationEachFifteen = 0
	while device_status_stop == 3:
		
		start=time.time()	
			
		esp_serial = str(ser.readline())
		sensor_buffer.append(esp_serial[2:][:-5] + ';'+ str(time.time_ns()*1000000))
			
		if len(sensor_buffer) %1000 == 0:
			print(len(sensor_buffer))
			iterationEachFifteen += 1
			
			#se sim, junta os 15k e envia
		if len(sensor_buffer) >= 15000:
				
				#print(time.time()-start)
				
				#print(len(sensor_buffer))
				#print(sensor_buffer[0])
				
			toSend = sensor_buffer.copy()

			if(is_online):
					
				print("online")
				t_http = Thread(target=sendJSONhttp, args=(toSend, http_lock))
				t_http.start()
				sensor_buffer.clear()		
				

							
			else:
					
				print("offline")
				t_log = Thread(target=write_log, args=(toSend, log_lock,))
				t_log.start()
				sensor_buffer.clear()
		
		if iterationEachFifteen == 15:
			iterationEachFifteen = 0
			device_status_stop = requests.get(url+'device_by_code/'+str(get_device_code('wlan0'))).json()["status_id"]
			
		
			

		
########################### GLOBAL VAR #################################


#url = 'https://enmpf6xid68v.x.pipedream.net/'
url = 'http://150.165.167.15:8100/'

#ser = serial.Serial("/dev/ttyS0", 921600)
ser = check_serial_ready()

ser.reset_input_buffer()
sensor_buffer = []

#is_online = requests.get(url+'device_by_code/'+str(get_device_code('wlan0')))

log_lock = Lock()
http_lock = Lock()

send_count =0

vehicleId = "-1"

############################ MAIN CODE #################################

#esp_serial = str(ser.readline())

# treinamento para novos veículos
compute_mean_dev()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
on_esp_flag = 0;

while True:
	
	online = True
	device = requests.get(url+'device_by_code/'+str(get_device_code('wlan0')))
	
	# se gpio18 estiver setado para 1 então coloque para 0
	if on_esp_flag == 1:
		GPIO.output(18, GPIO.LOW)
		on_esp_flag = 0
		print("esp32 deep sleep")
	
	if device.json()['status_id'] == 1:
		os.system("sudo ifconfig wlan0 down")
		os.system("sudo ifconfig eth0 down")
		#os.system("sudo vcgencmd display_power 0")
		# desligar usb
		#os.system('echo "0" | sudo tee /sys/us/usb/devices/1-1.3/authorized')
		print('off source')
		time.sleep(20)
		os.system("sudo ifconfig wlan0 up")
		os.system("sudo ifconfig eth0 up")
		#os.system("sudo vcgencmd display_power 1")
		# ligar usb
		#os.system('echo "1" | sudo tee /sys/bus/usb/devices/1-1.3/authorized')
		print('on source')
		
		continue
		
	elif device.json()['status_id'] == 2:
			
		item = {
			"device_code": str(get_device_code('wlan0')),
			"status_id": 3,
			"vehicle_id": str(device.json()["vehicle_id"])
		}
		json_i = JSON.dumps(item)
		requests.put(url+'device/', data=json_i, headers={"Content-Type":"application/json"})
		 
		
	elif device.json()['status_id'] == 3:
		print("começando a coleta")
		#setando gpio18 para 1
		GPIO.output(18, GPIO.HIGH)
		on_esp_flag = 1
		adxl_transmiter(device.json()['status_id'], online)

	
