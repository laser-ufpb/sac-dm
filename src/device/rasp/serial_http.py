import requests
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial("/dev/ttyS0", 9600)

url = 'https://enmpf6xid68v.x.pipedream.net/'
sensor_buffer = []

while 1:
    
    if len(sensor_buffer) == 10:
        break

    esp_serial = ser.readline()
    print(esp_serial)

    sensor_buffer.append(esp_serial)

    time.sleep(1)

x = requests.post(url, json={'data_rasp': sensor_buffer})

print(x.text)