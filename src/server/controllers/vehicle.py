import datetime
from models.models import Vehicle
from schemas.vehicle import VehicleSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_vehicle(vehicle_schema: VehicleSchema, db: Session):
    vehicle = Vehicle(**vehicle_schema.dict())
    db.add(vehicle)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered vehicle!")


def get_all_vehicles(db: Session):
    return db.query(Vehicle).all()


def get_vehicle(id: int, db: Session):
    if id:
        return db.query(Vehicle).filter(Vehicle.id == id).first()