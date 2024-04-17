from models.models import Status
from sqlalchemy.orm import Session
from schemas.status import StatusSchema
from fastapi import status
from fastapi.responses import JSONResponse


def create_status(status_schema: StatusSchema, db: Session):
    try:
        status_to_insert = Status(**status_schema.dict())
        db.add(status_to_insert)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successfully entered status data!")
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Failed to create status!")

def get_all_status(db: Session):
    return db.query(Status).all()