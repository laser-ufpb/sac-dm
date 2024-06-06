import datetime
from models.models import SACDM, Device
from schemas.sacdm import SACDMSchema
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status
from fastapi.responses import JSONResponse


def create_sacdm(sac_dm_schema: List[SACDMSchema], db: Session):
    try:
        aux = db.query(Device.vehicle_id).filter(Device.id == sac_dm_schema[0].device_id).first()
        sac_dm_data = [SACDM(**{**sac_dm.dict(), 'vehicle_id' : aux[0]}) for sac_dm in sac_dm_schema]
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


def get_sacdm_by_filter(vehicle_id: int, datetime_initial: str, datetime_final: str, db: Session):
    if vehicle_id and not datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.vehicle_id == vehicle_id).all()
    elif vehicle_id and datetime_initial and not datetime_final:
        return db.query(SACDM).filter(SACDM.vehicle_id == vehicle_id, SACDM.timestamp >= datetime_initial).all()
    elif vehicle_id and datetime_final and not datetime_initial:
        return db.query(SACDM).filter(SACDM.vehicle_id == vehicle_id, SACDM.timestamp <= datetime_final).all()
    elif vehicle_id and datetime_initial and datetime_final:
        return db.query(SACDM).filter(SACDM.vehicle_id == vehicle_id, SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()
    elif datetime_initial and not datetime_final and not vehicle_id:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial).all()
    elif datetime_final and not datetime_initial and not vehicle_id:
        return db.query(SACDM).filter(SACDM.timestamp <= datetime_final).all()
    elif datetime_initial and datetime_final and not vehicle_id:
        return db.query(SACDM).filter(SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final ).all()