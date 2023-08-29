import datetime
from models.models import Device
from schemas.device import DeviceSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_device(device_schema: DeviceSchema, db: Session):
    device = Device(**device_schema.dict())
    device.timestamp = datetime.datetime.now()
    db.add(device)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")

def get_all_devices(db: Session):
    return db.query(Device).all()
