import datetime
from models.models import Device
from schemas.device import DeviceSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_device(device_schema: DeviceSchema, db: Session):
    try:
        device = Device(**device_schema.dict())
        device.timestamp = datetime.datetime.now()
        db.add(device)
        db.commit()
    except Exception as e:
        if "foreign key" in str(e).lower():
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Invalid Vehicle or Status!"})
        else:
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to enter data!"})
            #return str(e)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully entered data!"})


def get_all_devices(db: Session):
    return db.query(Device).all()

def get_device(device_code: str, db: Session):
    if id:
        return db.query(Device).filter(Device.device_code == device_code).first()


def delete_a_device(device_code: str, db: Session):
    try:
        device = db.query(Device).filter(Device.device_code == device_code).first()
        if(not device):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Device not exist!"})
        db.delete(device)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Successfully deleted data!"})
    except Exception as e:
        if "foreign key" in str(e):
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Can't delete a device with registered data!"})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Delete failed!"})


def change_device_status(device_schema: DeviceSchema, db: Session):
    device = Device(**device_schema.dict())
    try:
        device = db.query(Device).filter(Device.device_code == device.device_code).first()
        if(not device):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Device not exist!"})
        if device_schema.status_id:
            device.status_id = device_schema.status_id
        if device_schema.vehicle_id:
            device.vehicle_id = device_schema.vehicle_id
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Successfully updated data!"})
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Update failed!"})