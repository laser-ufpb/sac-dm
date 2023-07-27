import datetime
from models.models import SACDM
from schemas.sacdm import SACDMSchema
from schemas.filter import Filter
from sqlalchemy.orm import Session
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse


def create_sacdm(sac_dm_schema: List[SACDMSchema], db: Session):
    sac_dm_data = [SACDM(**sac_dm.dict()) for sac_dm in sac_dm_schema]
    db.add_all(sac_dm_data)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")


def get_all_sacdm(db: Session):
    return db.query(SACDM).all()

    
def get_sacdm_by_device_id(data: Filter, db: Session):
    return db.query(SACDM).filter(SACDM.device_id == data.device_id).all()


def get_sacdm_by_datetime(data: Filter, db: Session):
    if data.datetime and not data.datetime_final:
        return db.query(SACDM).filter(SACDM.timestamp > data.datetime).all()
    else:
        return db.query(SACDM).filter(SACDM.timestamp > data.datetime, SACDM.timestamp < data.datetime_final ).all()
    
    
def get_sacdm_by_device_id_and_datetime(data: Filter, db: Session):
    if data.datetime and not data.datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == data.device_id, SACDM.timestamp > data.datetime).all()
    else:
        return db.query(SACDM).filter(SACDM.device_id == data.device_id, SACDM.timestamp > data.datetime, SACDM.timestamp < data.datetime_final ).all()
    