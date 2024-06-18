import sqlite3
import datetime
import json
import random
from models.models import Device, SACDM, AccelerometerAcquisition, LoginRequest, User, Status, Vehicle, SACDMDefault
from models.users import authenticate_user, get_current_user
from models.token import create_access_token
from schemas.accelerometer import AccelerometerSchema
from schemas.device import DeviceSchema
from schemas.sacdm import SACDMSchema
from schemas.status import StatusSchema
from schemas.user import UserSchema
from schemas.vehicle import VehicleSchema
from schemas.sacdm_default import SACDMDefaultSchema
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from typing_extensions import Annotated
from uuid import uuid4
from controllers.accelerometer import *
from controllers.device import create_device, get_all_devices, get_device, delete_a_device, change_device_status
from controllers.sac_dm import *
from controllers.status import create_status, get_all_status
from controllers.vehicle import *
from controllers.sacdm_default import *
from database import (get_db, Session)
from controllers.user import create_user, get_all_users, delete_user, get_user_by_username


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
    data: List[Device] = get_all_devices(db)
    return data


# Route to get device by device_code
@app.get("/device_by_code/{code}")
def get_device_by_code(code: str, db: Session=Depends(get_db)):
    data: Device = get_device(code, db)
    return data


# Route to insert a new data into the devices table
@app.post("/device")
def new_device(device: DeviceSchema, db: Session=Depends(get_db)):
    if (str(device.device_code).strip()):
        return create_device(device, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


# Route to delete data from devices table
@app.delete("/device/{device_code}")
def delete_device(device_code: str, db: Session=Depends(get_db)):
    return delete_a_device(device_code, db)


# Route to update status_id from a device
@app.put("/device")
def update_device_status(device: DeviceSchema, db: Session=Depends(get_db)):
    return change_device_status(device, db)


# Route to get all data from vehicle table
@app.get("/vehicle")
def get_vehicles(db: Session=Depends(get_db)):
    data: List[Vehicle] = get_all_vehicles(db)
    return data


# Route to get vehicle by id
@app.get("/vehicle_by_id/{id}")
def get_vehicle_by_id(id: int, db: Session=Depends(get_db)):
    data: Vehicle = get_vehicle(id, db)
    return data


# Route to insert a new data into the vehicle table
@app.post("/vehicle")
def new_vehicle(vehicle: VehicleSchema, db: Session=Depends(get_db)):
    if (str(vehicle.model).strip() and str(vehicle.manufacturer).strip()):
        return create_vehicle(vehicle, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


# Route to insert a new data into the status table
@app.post("/status")
def new_status(status: StatusSchema, db: Session=Depends(get_db)):
    return create_status(status, db)

# Route to get all data from status table
@app.get("/status")
def get_status(db: Session=Depends(get_db)):
    data: List[Status] = get_all_status(db)
    return data


# Route to get data from sac_dm table with an optional limit
@app.get("/sac_dm")
def get_sacdm(db: Session=Depends(get_db), limit: Optional[int] = Query(None, description="Limit the number of records returned")):
    data: List[SACDM] = get_all_sacdm(db,  limit)
    return data


# Route to get data from sac_dm table filtered by anything
@app.get("/sac_dm_by_filter")
def sacdm_by_filter(vehicle_id: Optional[int] = Query(None, description="Optional vehicle id for filter"),
                                    datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"),
                                    limit: Optional[int] = Query(None, description="Limit the number of records returned"),
                                    db: Session=Depends(get_db)):
    data: List[SACDM] = get_sacdm_by_filter(vehicle_id, datetime_initial, datetime_final, limit, db)
    return data


# Route to insert a new data into the sac_dm table
@app.post("/sac_dm")
def new_sacdm(sac_dm_data: List[SACDMSchema], db: Session=Depends(get_db)):
    return create_sacdm(sac_dm_data, db)


# Route to delete data from sacdm table by vehicle_id
@app.delete("/sacdm_by_vehicle_id/{vehicle_id}")
def delete_sacdm_by_vehicle_id(vehicle_id: int, db: Session=Depends(get_db)):
    return delete_sacdm_records_by_vehicle_id(vehicle_id, db)


# Route to delete data from sacdm table by datetime
@app.delete("/sacdm_by_datetime")
def delete_sacdm_by_datetime(datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"), 
                    db: Session=Depends(get_db)):
    return delete_sacdm_records_by_datetime(datetime_initial, datetime_final, db)


# Route to get all data from accelerometer table
@app.get("/accelerometer")
def get_accelerometter_data(db: Session=Depends(get_db)):
    registers: List[AccelerometerAcquisition] = get_all_accelerometer_records(db)
    return registers


# Route to get data from accelerometer table filtered by anything
@app.get("/accelerometer_by_filter")
def accelerometer_by_filter(device_id: Optional[int] = Query(None, description="Optional device id for filter"),
                                    datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"), 
                                    db: Session=Depends(get_db)):
    data: List[SACDM] = get_accelerometer_by_filter(device_id, datetime_initial, datetime_final, db)
    return data


# Route to insert data into accelerometer table
@app.post("/accelerometer")
def new_accelerometer_record(accelerometer_data: List[AccelerometerSchema], db: Session=Depends(get_db)):
    return create_accelerometer_record(accelerometer_data, db)


# Route to delete data from accelerometer table by device_code
@app.delete("/accelerometer_by_device_code/{device_code}")
def delete_accelerometer_by_device_id(device_code: str, db: Session=Depends(get_db)):
    return delete_accelerometer_records_by_device_code(device_code, db)


# Route to delete data from accelerometer table by datetime
@app.delete("/accelerometer_by_datetime")
def delete_accelerometer_by_datetime(datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"), 
                    db: Session=Depends(get_db)):
    return delete_accelerometer_records_by_datetime(datetime_initial, datetime_final, db)


# Route to get a data from SACDMDefault table by vehicle id
@app.get("/sacdm_default")
def all_sacdm_default(vehicle_id: Optional[int] = Query(None, description="vehicle_id to filter"), db: Session=Depends(get_db)):
    data: List[SACDMDefault] = get_sacdm_default(vehicle_id, db)
    return data


# Route to insert a new data into SACDMFedault table
@app.post("/sacdm_default")
def new_sacdm_default(data: SACDMDefaultSchema, db: Session = Depends(get_db)):
    return create_sacdm_default(data, db)


# Route to insert a new data into users table
@app.post("/user")
def new_user(user: UserSchema, db: Session = Depends(get_db)):
    return create_user(user, db)

@app.get("/user")
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@app.get("/user/{username}")
def get_user_by_username_route(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(username, db)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found!")
    return user


@app.delete("/user/delete/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)


@app.post("/login")
async def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        return JSONResponse(
            status_code=401,
            content="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
