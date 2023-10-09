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


def delete_a_device(device_schema: DeviceSchema, db: Session):
    device = Device(**device_schema.dict())
    try:
        device = db.query(Device).filter(Device.device_code == device.device_code).first()
        if(not device):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Device not exist!")
        db.delete(device)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successfully deleted data!")
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Delete failed!")
