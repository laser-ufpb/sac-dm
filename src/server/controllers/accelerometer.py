import datetime
from models.models import AccelerometerAcquisition, Device
from schemas.accelerometer import AccelerometerSchema
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


# def get_accelerometer_record_by_label(data: Filter, db: Session):
#     print("Data: ", data)
#     if data.label:
#         return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.label == data.label).all()


def get_accelerometer_by_filter(device_id: int, datetime_initial: str, datetime_final: str, db: Session):
    if device_id and not datetime_initial and not datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id).all()
    elif device_id and datetime_initial and not datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id, AccelerometerAcquisition.timestamp >= datetime_initial).all()
    elif device_id and datetime_final and not datetime_initial:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id, AccelerometerAcquisition.timestamp <= datetime_final).all()
    elif device_id and datetime_initial and datetime_final:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id, AccelerometerAcquisition.timestamp >= datetime_initial, AccelerometerAcquisition.timestamp <= datetime_final ).all()
    elif datetime_initial and not datetime_final and not device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= datetime_initial).all()
    elif datetime_final and not datetime_initial and not device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp <= datetime_final).all()
    elif datetime_initial and datetime_final and not device_id:
        return db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= datetime_initial, AccelerometerAcquisition.timestamp <= datetime_final ).all()


def delete_accelerometer_records_by_device_code(device_code: int, db: Session):
    device_id = db.query(Device.id).filter(Device.device_code == device_code).first()
    try:
        records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.device_id == device_id[0]).all()
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
    

def delete_accelerometer_records_by_datetime(datetime_initial: str, datetime_final: str, db: Session):
    if datetime_initial and not datetime_final:
        try:
            records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= datetime_initial).all()
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
    elif datetime_final and not datetime_initial:
        try:
            records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp <= datetime_final).all()
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
    elif datetime_initial and datetime_final:
        try:
            records = db.query(AccelerometerAcquisition).filter(AccelerometerAcquisition.timestamp >= datetime_initial, AccelerometerAcquisition.timestamp <= datetime_final).all()
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
