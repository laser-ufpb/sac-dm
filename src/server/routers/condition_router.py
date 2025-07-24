from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.condition import *
from schemas.condition import ConditionSchema
from database import get_db

router = APIRouter(prefix="/condition", tags=["Condition"])

# Route to insert a new data into the condition table
@router.post("/condition")
async def new_condition(condition: ConditionSchema, db: Session=Depends(get_db)):
    return create_condition(condition, db)


# Route to get all data from condition table
@router.get("/condition")
async def get_condition(db: Session=Depends(get_db)):
    data: List[Condition] = get_all_condition(db)
    return data