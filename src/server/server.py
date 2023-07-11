import sqlite3
import datetime
import json
import random
from models.models import Device, SACDM, AccelerometerAcquisition, LoginRequest
from models.users import authenticate_user, get_current_user
from models.token import create_access_token
from schemas.device import DeviceSchema
from schemas.sacdm import SACDMSchema
from schemas.accelerometer import AccelerometerSchema
from schemas.filter import Filter
from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from typing_extensions import Annotated
from uuid import uuid4
from controllers.device import create_device, get_all_devices
from controllers.sac_dm import create_sacdm, get_all_sacdm, get_sacdm_with_filter
from controllers.accelerometer import create_accelerometer_record, get_all_accelerometer_records, get_accelerometer_record_by_id
from database import (get_db, Session)


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

# Route to get all data from device table
@app.get("/device")
def get_devices(db: Session=Depends(get_db)):
    banco_dados: List[Device] = get_all_devices(db)
    return banco_dados


# Route to insert a new data into the devices table
@app.post("/device")
def new_device(device: DeviceSchema, db: Session=Depends(get_db)):
    if (str(device.device_code).strip()):
        return create_device(device, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


# Route to get all data from sac_dm table
@app.get("/sac_dm")
def get_sacdm(db: Session=Depends(get_db)):
    banco_dados: List[SACDM] = get_all_sacdm(db)
    return banco_dados


# Route to get data from sac_dm table with a filter
@app.get("/sac_dm_with_filter")
def get_sacdm_filtered(data: Filter, db: Session=Depends(get_db)):
    banco_dados: List[SACDM] = get_sacdm_with_filter(data, db)
    return banco_dados


# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_datas: List[SACDMSchema], db: Session=Depends(get_db)):
    results = []
    for data in sac_dm_datas:
        if (str(data.device_id).strip()):
            try:
                result = create_sacdm(data, db)
                results.append(result)
            except Exception as e:
                db.rollback()
                results.append(f"Error: {str(e)}")
        else:
            results.append("Invalid data!")        
    return results


# Route to get all data from accelerometer table
@app.get("/accelerometer")
def get_accelerometter_data(db: Session=Depends(get_db)):
    registers: List[AccelerometerAcquisition] = get_all_accelerometer_records(db)
    return registers


# Route to get data from sac_dm table with a specifit device_id
@app.get("/accelerometer_by_device_id")
def get_accelerometer_by_device_id(data: Filter, db: Session=Depends(get_db)):
    banco_dados: List[AccelerometerAcquisition] = get_accelerometer_record_by_id(data.device_id, db)
    return banco_dados


# Route to insert a new data into the accelerometer table
@app.post("/accelerometer")
def new_accelerometer_record(accelerometer_data: List[AccelerometerSchema], db: Session=Depends(get_db)):
    results = []
    for data in accelerometer_data:
        if (str(data.device_id).strip()):
            try:
                result = create_accelerometer_record(data, db)
                results.append(result)
            except Exception as e:
                db.rollback()
                results.append(f"Error: {str(e)}")
        else:
            results.append("Invalid data!")
    
    return results


@app.post("/login")
async def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        return JSONResponse(
            status_code=401,
            content="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
