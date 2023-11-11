import paho.mqtt.client as mqtt
import requests
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial("/dev/ttyS0", 9600)

sensor_buffer = []


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("/aviacao")


def on_publish(client, userdata, result):
    print("data published \n")
    pass


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def store_variable_in_file(variable, filename):
    with open(filename, 'w') as file:
        file.write(str(variable))


while 1:

    if len(sensor_buffer) == 10:
        break

    esp_serial = ser.readline()
    print(esp_serial)

    sensor_buffer.append(esp_serial)

    time.sleep(1)

client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
file_name = 'output.txt'
store_variable_in_file(sensor_buffer, file_name)
ret = client.publish("/aviacao", sensor_buffer)
print(ret.text)
client.loop_forever()
