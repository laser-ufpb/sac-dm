import sqlite3
import datetime
import json
import random
from models.models import Device, SACDM, AccelerometerData, LoginRequest
from models.users import authenticate_user, get_current_user
from models.token import create_access_token
from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from typing_extensions import Annotated
from uuid import uuid4
from database import insert_data_device, insert_data_sac_dm, insert_data_accelerometer_register, get_all_data, get_all_accelerometer_data, create_db

app = FastAPI()
create_db()

origins = ['*', 'http://localhost:8000']
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
def new_device(device: Device):
    device.time_stamp = datetime.datetime.now()
    if (str(device.device_code).strip()):
        return insert_data_device((device.device_code, device.time_stamp))
    return JSONResponse(status_code=500, content="Invalid data!")


# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_data: SACDM):
    sac_dm_data.time_stamp = datetime.datetime.now()
    return insert_data_sac_dm(
        (sac_dm_data.value,
         sac_dm_data.device_code,
         sac_dm_data.time_stamp))


# Route to insert a new data into the accelerometer_register table
@app.post("/accelerometer")
def new_accelerometer_data(accelerometer_data: AccelerometerData):
    return insert_data_accelerometer_register(
        (accelerometer_data.device_code,
         accelerometer_data.time_stamp,
         accelerometer_data.ACx,
         accelerometer_data.ACy,
         accelerometer_data.ACz))


@app.get("/device")
def get_devices():
    banco_dados: List[Device] = get_all_data()
    return banco_dados


@app.get("/accelerometer")
def get_accelerometter_data():
    registers: List[AccelerometerData] = get_all_accelerometer_data()
    return registers


@app.post("/login")
def login(login_request: LoginRequest):
    print("Back login")
    if login_request.username == "admin" and login_request.password == "admin":
        return {"success": True, "message": "Login realizado com sucesso"}
    else:
        return JSONResponse(
            status_code=401,
            content="Usuário ou senha incorretos")


@app.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=401,
            content="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
