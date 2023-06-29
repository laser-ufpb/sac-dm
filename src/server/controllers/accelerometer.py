import datetime
from models.models import AccelerometerAcquisition
from schemas.accelerometer import AccelerometerSchema
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
