import datetime
from models.models import AccelerometerAcquisition
from schemas.accelerometer import AccelerometerSchema
from schemas.filter import Filter
from sqlalchemy.orm import Session
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse


def create_accelerometer_record(accelerometer_schema: List[AccelerometerSchema], db: Session):
    try:
        records = [AccelerometerAcquisition(**accelerometer_record.dict()) for accelerometer_record in accelerometer_schema]
        db.add_all(records)
        db.commit()
    except Exception:
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Failed to insert data to the database."}
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")

def get_all_accelerometer_records(db: Session):
    return db.query(AccelerometerAcquisition).all()

    
def get_accelerometer_record_by_device_id(data: Filter, db: Session):
    if data.device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == data.device_id).all()

def get_accelerometer_record_by_label(data: Filter, db: Session):
    print("Data: ", data)
    if data.label:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.label == data.label).all()

def get_accelerometer_record_by_datetime(data: Filter, db: Session):
    if data.datetime_initial and not data.datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= data.datetime_initial).all()
    elif data.datetime_initial and data.datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= data.datetime_initial, AccelerometerAcquisition.timestamp <= data.datetime_final).all()
    

def get_accelerometer_record_by_device_id_and_datetime(data: Filter, db: Session):
    if data.device_id and data.datetime_initial and not data.datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == data.device_id, AccelerometerAcquisition.timestamp >= data.datetime_initial).all()
    elif data.device_id and data.datetime_initial and data.datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == data.device_id, AccelerometerAcquisition.timestamp >= data.datetime_initial, AccelerometerAcquisition.timestamp <= data.datetime_final).all()
 

def delete_accelerometer_records_by_device_id(device_id_filter: Filter, db: Session):
    try:
        records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id_filter.device_id).all()
        if(not records):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Device don't have logs!")
        for record in records:
            db.delete(record)            
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successfully deleted data!")
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Delete failed!")
    

def delete_accelerometer_records_by_datetime(device_datetime_filter: Filter, db: Session):
    if device_datetime_filter.datetime_initial and not device_datetime_filter.datetime_final:
        try:
            records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= device_datetime_filter.datetime_initial).all()
            if(not records):
                return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Datetime don't have logs!")
            for record in records:
                db.delete(record)            
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Successfully deleted data!")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Delete failed!")
    elif device_datetime_filter.datetime_initial and device_datetime_filter.datetime_final:
        try:
            records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= device_datetime_filter.datetime_initial, AccelerometerAcquisition.timestamp <= device_datetime_filter.datetime_final).all()
            if(not records):
                return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Datetime don't have logs!")
            for record in records:
                db.delete(record)            
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Successfully deleted data!")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Delete failed!")
