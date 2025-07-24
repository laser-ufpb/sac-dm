from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.vehicle import *
from schemas.vehicle import VehicleSchema
from database import get_db

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])

# Route to get all data from vehicle table
@router.get("/vehicle")
async def get_vehicles(db: Session=Depends(get_db)):
    data: List[Vehicle] = get_all_vehicles(db)
    return data


# Route to get vehicle by id
@router.get("/vehicle_by_id/{id}")
async def get_vehicle_by_id(id: int, db: Session=Depends(get_db)):
    data: Vehicle = get_vehicle(id, db)
    return data


# Route to insert a new data into the vehicle table
@router.post("/vehicle")
async def new_vehicle(vehicle: VehicleSchema, db: Session=Depends(get_db)):
    if (str(vehicle.model).strip() and str(vehicle.manufacturer).strip()):
        return create_vehicle(vehicle, db)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Invalid data!")


# Route to delete data from vehicle table
@router.delete("/vehicle/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Session=Depends(get_db)):
    return delete_a_vehicle(vehicle_id, db)