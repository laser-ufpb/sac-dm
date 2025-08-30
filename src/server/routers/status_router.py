from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.status import *
from schemas.status import StatusSchema
from database import get_db

router = APIRouter(tags=["Status"])

# Route to insert a new data into the status table
@router.post("/status")
async def new_status(status: StatusSchema, db: Session=Depends(get_db)):
    return create_status(status, db)


# Route to get all data from status table
@router.get("/status")
async def get_status(db: Session=Depends(get_db)):
    data: List[Status] = get_all_status(db)
    return data