import datetime
from models.models import SACDMDefault
from schemas.sacdm_default import SACDMDefaultSchema
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status
from fastapi.responses import JSONResponse

def get_sacdm_default(vehicle_id: int, db: Session, limit: Optional[int] = None):
    data = db.query(SACDMDefault).filter(SACDMDefault.vehicle_id == vehicle_id).order_by(desc(SACDMDefault.id)).first()
    return data


def create_sacdm_default(sacdm_default_schema: SACDMDefaultSchema, db: Session):
    try:
        data = SACDMDefault(**sacdm_default_schema.dict())
        db.add(data)
        db.commit()
    except Exception:
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Failed to insert data to the database."}
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")