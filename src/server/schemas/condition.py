from pydantic import BaseModel


class ConditionSchema(BaseModel):
    description: str