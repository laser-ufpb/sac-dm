import datetime
from models.models import SACDM
from schemas.sacdm import SACDMSchema
from schemas.filter import Filter
from sqlalchemy.orm import Session
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse


def create_sacdm(sac_dm_schema: List[SACDMSchema], db: Session):
    try:
        sac_dm_data = [SACDM(**sac_dm.dict()) for sac_dm in sac_dm_schema]
        db.add_all(sac_dm_data)
        db.commit()
    except Exception:
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Failed to insert data to the database."}
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")


def get_all_sacdm(db: Session):
    return db.query(SACDM).all()

    
def get_sacdm_by_device_id(data: int, db: Session):
    if data:
        return db.query(SACDM).filter(SACDM.device_id == data).all()


def get_sacdm_by_datetime(data: Filter, db: Session):
    if data.datetime_initial and not data.datetime_final:
        return db.query(SACDM).filter(SACDM.timestamp >= data.datetime_initial).all()
    elif data.datetime_initial and data.datetime_final:
        return db.query(SACDM).filter(SACDM.timestamp >= data.datetime_initial, SACDM.timestamp <= data.datetime_final ).all()
    
    
def get_sacdm_by_device_id_and_datetime(data: Filter, db: Session):
    if data.device_id and data.datetime_initial and not data.datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == data.device_id, SACDM.timestamp >= data.datetime_initial).all()
    elif data.device_id and data.datetime_initial and data.datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == data.device_id, SACDM.timestamp >= data.datetime_initial, SACDM.timestamp <= data.datetime_final ).all()
    