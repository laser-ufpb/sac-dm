import sqlite3
import datetime
import json
import random
from models.models import Device, SACDM, AccelerometerAcquisition, LoginRequest
from models.users import authenticate_user, get_current_user
from models.token import create_access_token
from schemas.device import DeviceSchema
from schemas.sacdm import SACDMSchema
from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from typing_extensions import Annotated
from uuid import uuid4
from controllers.device import create_device, get_all_devices
from database import (insert_data_sac_dm,insert_data_accelerometer_register,
 get_all_data, get_all_accelerometer_acquisition, get_db, Session)


app = FastAPI()

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
def new_device(device: DeviceSchema, db: Session=Depends(get_db)):
    if (str(device.device_code).strip()):
        return create_device(device, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


@app.get("/device")
def get_devices(db: Session=Depends(get_db)):
    banco_dados: List[Device] = get_all_devices(db)
    return banco_dados


# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_data: SACDMSchema):
    sacdm = SACDM(device_id=sac_dm_data.device_id, value=sac_dm_data.value)
    sacdm.timestamp = datetime.datetime.now()
    return insert_data_sac_dm(
        (sacdm.value,
         sacdm.device_id,
         sacdm.timestamp))


# Route to insert a new data into the accelerometer_register table
# @app.post("/accelerometer")
# def new_accelerometer_data(accelerometer_data: AccelerometerAcquisition):
#     return insert_data_accelerometer_register(
#         (accelerometer_data.device_id,
#          accelerometer_data.timestamp,
#          accelerometer_data.ACx,
#          accelerometer_data.ACy,
#          accelerometer_data.ACz))


@app.get("/accelerometer")
def get_accelerometter_data():
    registers: List[AccelerometerAcquisition] = get_all_accelerometer_acquisition()
    return registers


@app.post("/login")
async def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        return JSONResponse(
            status_code=401,
            content="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
