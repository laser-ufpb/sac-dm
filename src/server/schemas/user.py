from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: Optional[bool] = None
    hashed_password: Optional[str]
