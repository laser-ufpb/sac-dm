from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from database import insert_data_device, insert_data_sac_dm, insert_data_accelerometer_register #, delete_data, update_data
import sqlite3
import datetime

app = FastAPI()

origins =['http://127.0.0.1:5500']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# New class for the devices data
class devices(BaseModel):
    device_code: Optional[str]
    time_stamp: Optional[str]

# New class for the sac_dm datas
class sac_dm_data(BaseModel):
    device_code: Optional[str]
    time_stamp: Optional[str]
    value: Optional[int]


# New class for the accelerometer data
class accelerometer_data(BaseModel):
    device_code: Optional[str]
    time_stamp: Optional[str]
    ACx: Optional[float]
    ACy: Optional[float]
    ACz: Optional[float]

@app.get("/")
def show_devices():
    return {"SUCCESS"}

# Route to insert a new data into the devices table
@app.post("/device")
def new_device(device: devices):
    #device.device_code = "MAC123"
    device.time_stamp = datetime.date.today()
    
    insert_data_device((device.device_code, device.time_stamp))

    return device

# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_data: sac_dm_data):
    #sac_dm_data.device_code = "MAC234"
    sac_dm_data.time_stamp = datetime.date.today()
    sac_dm_data.value = random.randint(1,8)
    
    insert_data_sac_dm((sac_dm_data.value, sac_dm_data.device_code, sac_dm_data.time_stamp))

    return sac_dm_data

# Route to insert a new data into the accelerometer_register table
@app.post("/accelerometer")
def new_accelerometer_data(accelerometer_data: accelerometer_data):
    #accelerometer_data.device_code = "MAC345"
    accelerometer_data.time_stamp = datetime.date.today()
    accelerometer_data.ACx = round(random.uniform(100,200), 3)
    accelerometer_data.ACy = round(random.uniform(100,200), 3)
    accelerometer_data.ACz = round(random.uniform(100,200), 3)
    
    insert_data_accelerometer_register((accelerometer_data.device_code, accelerometer_data.time_stamp, accelerometer_data.ACx, accelerometer_data.ACy, accelerometer_data.ACz))

    return accelerometer_data



#banco_dados: List[devices] = []
#ids_cadastrados = []

#@app.get("/dispositivos")
#def mostrar_dispositivos():
#    return banco_dados

#@app.delete("/dispositivos/{id}")
#def deletar_dispositivo(id: str):
#    # Verifica se o id existe no banco de dados
#    if not any(disp.id == id for disp in banco_dados):
#        return {"message": "Dispositivo não encontrado"}
#
#    # Remove o dispositivo do banco de dados
#    delete_data(id)
#
#    # Remove o dispositivo da lista de dispositivos
#    banco_dados[:] = [disp for disp in banco_dados if disp.id != id]
#
#   return {"message": "Dispositivo removido com sucesso"}


#@app.put("/dispositivos/{id}/{new_dens}")
#def update(id: int, new_dens: int):
#    update_data(id, new_dens)