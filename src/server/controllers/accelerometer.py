import datetime
from models.models import AccelerometerAcquisition
from schemas.accelerometer import AccelerometerSchema
from schemas.filter import Filter
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_accelerometer_record(accelerometer_schema: AccelerometerSchema, db: Session):
    record = AccelerometerAcquisition(**accelerometer_schema.dict())
    record.timestamp = datetime.datetime.now()
    db.add(record)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")

def get_all_accelerometer_records(db: Session):
    return db.query(AccelerometerAcquisition).all()

def get_accelerometer_record_with_filter(data: Filter, db: Session):
    if data.datetime and data.device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp > data.datetime).filter(AccelerometerAcquisition.device_id == data.device_id).all()
    elif data.device_id and not data.datetime:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == data.device_id).all()
    elif data.datetime and not data.device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp > data.datetime).all()