from pydantic import BaseModel


class StatusSchema(BaseModel):
    description: str