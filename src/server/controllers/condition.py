from models.models import Condition
from sqlalchemy.orm import Session
from schemas.condition import ConditionSchema
from fastapi import status
from fastapi.responses import JSONResponse


def create_condition(condition_schema: ConditionSchema, db: Session):
    try:
        condition_to_insert = Condition(**condition_schema.dict())
        db.add(condition_to_insert)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Successfully entered condition data!"})
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to create condition!"})

async def get_all_condition(db: Session):
    return db.query(Condition).all()