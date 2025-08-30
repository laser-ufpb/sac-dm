from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.sac_dm import *
from controllers.sacdm_default import *
from schemas.sacdm import SACDMSchema
from schemas.sacdm_default import SACDMDefaultSchema
from database import get_db

router = APIRouter(tags=["SACDM"])

# Route to get data from sac_dm table with an optional limit
@router.get("/sac_dm")
async def get_sacdm(db: Session=Depends(get_db), limit: Optional[int] = Query(None, description="Limit the number of records returned")):
    data: List[SACDM] = get_all_sacdm(db,  limit)
    return data


# Route to get data from sac_dm table filtered by anything
@router.get("/sac_dm_by_filter")
async def sacdm_by_filter(vehicle_id: Optional[int] = Query(None, description="Optional vehicle id for filter"),
                                    datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"),
                                    limit: Optional[int] = Query(None, description="Limit the number of records returned"),
                                    db: Session=Depends(get_db)):
    data: List[SACDM] = get_sacdm_by_filter(vehicle_id, datetime_initial, datetime_final, limit, db)
    return data


# Route to insert a new data into the sac_dm table
@router.post("/sac_dm")
async def new_sacdm(sac_dm_data: List[SACDMSchema], db: Session=Depends(get_db)):
    return create_sacdm(sac_dm_data, db)


# Route to delete data from sacdm table by vehicle_id
@router.delete("/sacdm_by_vehicle_id/{vehicle_id}")
async def delete_sacdm_by_vehicle_id(vehicle_id: int, db: Session=Depends(get_db)):
    return delete_sacdm_records_by_vehicle_id(vehicle_id, db)


# Route to delete data from sacdm table by datetime
@router.delete("/sacdm_by_datetime")
async def delete_sacdm_by_datetime(datetime_initial: Optional[str] = Query(None, description="Optional initial datetime"),
                    datetime_final: Optional[str] = Query(None, description="Optional final datetime"), 
                    db: Session=Depends(get_db)):
    return delete_sacdm_records_by_datetime(datetime_initial, datetime_final, db)


# Route to get a data from SACDMDefault table by vehicle id
@router.get("/sacdm_default")
async def all_sacdm_default(vehicle_id: Optional[int] = Query(None, description="vehicle_id to filter"), db: Session=Depends(get_db)):
    data: List[SACDMDefault] = get_sacdm_default(vehicle_id, db)
    return data


# Route to insert a new data into SACDMFedault table
@router.post("/sacdm_default")
async def new_sacdm_default(data: SACDMDefaultSchema, db: Session = Depends(get_db)):
    return create_sacdm_default(data, db)