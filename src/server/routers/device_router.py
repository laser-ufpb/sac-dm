from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.device import (
    get_all_devices, get_device, create_device,
    delete_a_device, change_device_status
)
from schemas.device import DeviceSchema
from database import get_db

router = APIRouter(prefix="/device", tags=["Device"])


# Route to get all data from device table
@router.get("/device")
async def get_devices(db: Session=Depends(get_db)):
    data: List[Device] = get_all_devices(db)
    return data


# Route to get device by device_code
@router.get("/device_by_code/{code}")
async def get_device_by_code(code: str, db: Session=Depends(get_db)):
    data: Device = get_device(code, db)
    return data


# Route to insert a new data into the devices table
@router.post("/device")
async def new_device(device: DeviceSchema, db: Session=Depends(get_db)):
    if (str(device.device_code).strip()):
        return create_device(device, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


# Route to delete data from devices table
@router.delete("/device/{device_code}")
async def delete_device(device_code: str, db: Session=Depends(get_db)):
    return delete_a_device(device_code, db)


# Route to update status_id from a device
@router.put("/device")
async def update_device_status(device: DeviceSchema, db: Session=Depends(get_db)):
    return change_device_status(device, db)