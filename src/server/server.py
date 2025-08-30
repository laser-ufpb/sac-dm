# Built-in
import datetime
import json
import random
import sqlite3
from uuid import uuid4

# Typing
from typing import List, Optional
from typing_extensions import Annotated

# FastAPI
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# App - Database
from database import get_db, Session

# App - Models
from models.models import (
    Condition,
    Device,
    SACDM,
    SACDMDefault,
    Status,
    User,
    Vehicle,
    LoginRequest,
    AccelerometerAcquisition
)
from models.token import create_access_token
from models.users import authenticate_user, get_current_user

# Schemas
from schemas.user import UserSchema
from schemas.accelerometer import AccelerometerSchema

# Controllers

from controllers.fault import get_log
from controllers.accelerometer import *
from controllers.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_username,
)

# Routers
from routers.device_router import router as device_router
from routers.vehicle_router import router as vehicle_router
from routers.sac_dm_router import router as sacdm_router
from routers.status_router import router as status_router
from routers.condition_router import router as condition_router


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
def default_page():
    return {"SUCCESS"}


app.include_router(device_router)
app.include_router(vehicle_router)
app.include_router(sacdm_router)
app.include_router(status_router)
app.include_router(condition_router)


# Route to get log by vehicle_id
@app.get("/log_by_vehicle_id/{id}")
def get_log_by_vehicle_id(id: int, db: Session=Depends(get_db)):
    data: List[Log] = get_log(id, db)
    return data


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