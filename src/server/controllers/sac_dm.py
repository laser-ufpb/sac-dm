import datetime
from models.models import SACDM
from schemas.sacdm import SACDMSchema
from schemas.filter import Filter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
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


def get_all_sacdm(db: Session, limit: Optional[int] = None):
    query = db.query(SACDM).order_by(desc(SACDM.timestamp))
    if limit:
        query = query.limit(limit)
    return query.all()


def get_sacdm_by_device_id(data: int, db: Session):
    if data:
        return db.query(SACDM).filter(SACDM.device_id == data).all()


def get_sacdm_by_datetime(datetime_initial: str, datetime_final: str, db: Session):
    if datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial).all()
    elif datetime_final and not datetime_initial:
        return db.query(SACDM).filter(SACDM.timestamp <= datetime_final).all()
    elif datetime_initial and datetime_final:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()
    
    
def get_sacdm_by_device_id_and_datetime(device_id: int, datetime_initial: str, datetime_final: str, db: Session):
    if device_id and datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == device_id, SACDM.timestamp >= datetime_initial).all()
    elif device_id and datetime_initial and datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == device_id, SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()
    

def get_sacdm_by_filter(device_id: int, datetime_initial: str, datetime_final: str, db: Session):
    if device_id and not datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == device_id).all()
    elif device_id and datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == device_id, SACDM.timestamp >= datetime_initial).all()
    elif device_id and datetime_final and not datetime_initial:
        return db.query(SACDM).filter(SACDM.device_id == device_id, SACDM.timestamp <= datetime_final).all()
    elif device_id and datetime_initial and datetime_final:
        return db.query(SACDM).filter(SACDM.device_id == device_id, SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()
    elif datetime_initial and not datetime_final and not device_id:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial).all()
    elif datetime_final and not datetime_initial and not device_id:
        return db.query(SACDM).filter(SACDM.timestamp <= datetime_final).all()
    elif datetime_initial and datetime_final and not device_id:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()