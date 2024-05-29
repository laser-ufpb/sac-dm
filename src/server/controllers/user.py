from models.models import User
from models.users import get_password_hash, verify_password
from schemas.user import UserSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

def create_user(user_schema: UserSchema, db: Session):
    user = User(**user_schema.dict())
    user.hashed_password = get_password_hash(user.hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Successfully entered data!")

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return JSONResponse(status_code=404, content="User not found")

    db.delete(user)
    db.commit()

    return JSONResponse(status_code=200, content="User deleted successfully")

def get_user_by_username(user: UserSchema, db: Session):
    user = db.query(User).filter(User.username == user).first()
    if not user:
        return JSONResponse(status_code=404, content="User not found")
    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }



def get_all_users(db: Session):
    users = db.query(User).all()
    return [
        {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
        }
        for user in users
    ]