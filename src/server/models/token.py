import os
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt


# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar o valor de SECRET_KEY
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def create_access_token(data: dict):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
