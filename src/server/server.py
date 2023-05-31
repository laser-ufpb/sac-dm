import sqlite3
import datetime
import json
import random
from classes import Devices, Sac_dm_data, Accelerometer_data
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from database import insert_data_device, insert_data_sac_dm, insert_data_accelerometer_register, get_all_data, get_all_accelerometer_data, create_db

app = FastAPI()
create_db()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def show_devices():
    return {"SUCCESS"}


# Route to insert a new data into the devices table
@app.post("/device")
def new_device(device: Devices):
    device.time_stamp = datetime.datetime.now()
    return insert_data_device((device.device_code, device.time_stamp))


# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_data: Sac_dm_data):
    sac_dm_data.time_stamp = datetime.datetime.now()
    if (str(sac_dm_data.value).strip()):
        return insert_data_sac_dm((sac_dm_data.value, sac_dm_data.device_code, sac_dm_data.time_stamp))


# Route to insert a new data into the accelerometer_register table
@app.post("/accelerometer")
def new_accelerometer_data(accelerometer_data: Accelerometer_data):
    if(str(accelerometer_data.ACx).strip() and str(accelerometer_data.ACy).strip() and str(accelerometer_data.ACz).strip()):
        return insert_data_accelerometer_register((accelerometer_data.device_code, accelerometer_data.time_stamp, accelerometer_data.ACx, accelerometer_data.ACy, accelerometer_data.ACz))
    return Response(status=500, response="Dados inválidos")


@app.get("/device")
def get_devices():
    banco_dados: List[Devices] = get_all_data()
    return banco_dados


@app.get("/accelerometer")
def get_accelerometter_data():
    registers: List[Accelerometer_data] = get_all_accelerometer_data()
    return registers
