import datetime
from models.models import Vehicle, Device
from schemas.vehicle import VehicleSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_vehicle(vehicle_schema: VehicleSchema, db: Session):
    try:
        vehicle = Vehicle(**vehicle_schema.dict())
        db.add(vehicle)
        db.commit()
    except Exception as e:
        if "foreign key" in str(e).lower():
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Invalid Status!")
        else:
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Failed to enter data!")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered vehicle!")


def get_all_vehicles(db: Session):
    return db.query(Vehicle).all()


def get_vehicle(id: int, db: Session):
    if id:
        return db.query(Vehicle).filter(Vehicle.id == id).first()
    

def delete_a_vehicle(vehicle_id: int, db: Session):
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

        if(not vehicle):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Vehicle not exist!")
        
        db.query(Device).filter(Device.vehicle_id == vehicle_id).update({"vehicle_id": None})

        db.delete(vehicle)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successfully deleted data, and related devices were unlinked!")
    except Exception as e:
        if "foreign key" in str(e):
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Can't delete a vehicle with registered data!")
        else:
            return str(e)
            #return JSONResponse(
            #tatus_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #content="Delete failed!")