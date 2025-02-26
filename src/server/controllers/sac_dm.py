import datetime
from models.models import SACDM, SACDMDefault, Device, Log
from schemas.sacdm import SACDMSchema
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status
from fastapi.responses import JSONResponse

from schemas.log import LogSchema
from controllers.fault import log_verifier

import sys
import os
sys.path.append(os.path.abspath("../sac-dm/"))
from util import classification


def create_sacdm(sac_dm_schema: List[SACDMSchema], db: Session):
    try:
        vehicle_id_query = db.query(Device.vehicle_id).filter(Device.id == sac_dm_schema[0].device_id).first()
        sac_dm_data = [SACDM(**{**sac_dm.dict(), 'vehicle_id' : vehicle_id_query[0]}) for sac_dm in sac_dm_schema]
        db.add_all(sac_dm_data)
        db.commit()
    except Exception:
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Failed to insert data to the database."}
    )
    return log_verifier(sac_dm_data, db)


def get_all_sacdm(db: Session, limit: Optional[int] = None):
    query = db.query(SACDM).order_by(desc(SACDM.timestamp))
    if limit:
        query = query.limit(limit)
    return query.all()


def get_sacdm_by_filter(vehicle_id: int, datetime_initial: str, datetime_final: str, limit: int, db: Session):
    query = db.query(SACDM).order_by(desc(SACDM.id))
    if vehicle_id:
        query = query.filter(SACDM.vehicle_id == vehicle_id)
    if datetime_initial:
        query = query.filter(SACDM.timestamp >= datetime_initial)
    if datetime_final:
        query = query.filter(SACDM.timestamp <= datetime_final)
    if limit:
        query = query.limit(limit)
    return query.all()
    

def delete_sacdm_records_by_vehicle_id(vehicle_id: int, db: Session):
    try:
        records = db.query(SACDM).filter(SACDM.vehicle_id == vehicle_id).all()
        if(not records):
            return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Vehicle don't have logs!")
        for record in records:
            db.delete(record)            
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successfully deleted data!")
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Delete failed!")
    

def delete_sacdm_records_by_datetime(datetime_initial: str, datetime_final: str, db: Session):
    if datetime_initial and not datetime_final:
        try:
            records = db.query(SACDM).filter(SACDM.timestamp >= datetime_initial).all()
            if(not records):
                return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Datetime don't have logs!")
            for record in records:
                db.delete(record)            
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Successfully deleted data!")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Delete failed!")
    elif datetime_final and not datetime_initial:
        try:
            records = db.query(SACDM).filter(SACDM.timestamp <= datetime_final).all()
            if(not records):
                return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Datetime don't have logs!")
            for record in records:
                db.delete(record)            
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Successfully deleted data!")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Delete failed!")
    elif datetime_initial and datetime_final:
        try:
            records = db.query(SACDM).filter(SACDM.timestamp >= datetime_initial, SACDM.timestamp <= datetime_final).all()
            if(not records):
                return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content="Datetime don't have logs!")
            for record in records:
                db.delete(record)            
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Successfully deleted data!")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Delete failed!")