import datetime
from models.models import SACDM
from schemas.sacdm import SACDMSchema
from schemas.filter import Filter
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_sacdm(sac_dm_schema: SACDMSchema, db: Session):
    sac_dm_data = SACDM(**sac_dm_schema.dict())
    sac_dm_data.timestamp = datetime.datetime.now()
    db.add(sac_dm_data)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")

def get_all_sacdm(db: Session):
    return db.query(SACDM).all()

def get_sacdm_with_filter(data: Filter, db: Session):
    if data.datetime and data.device_id:
        return db.query(SACDM).filter(SACDM.timestamp > data.datetime).filter(SACDM.device_id == data.device_id).all()
    elif data.device_id and not data.datetime:
        return db.query(SACDM).filter(SACDM.device_id == data.device_id).all()
    elif data.datetime and not data.device_id:
        return db.query(SACDM).filter(SACDM.timestamp > data.datetime).all()