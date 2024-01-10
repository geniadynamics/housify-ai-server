from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType
from datetime import datetime

from tortoise.fields.data import UUIDField


class RequestSchema(BaseModel):
    user: Optional[str] = Field()

    input: str = Field()

    img_input: Optional[str] = Field(None, max_length=256)
    img_output: Optional[str] = Field(None, max_length=256)

    output_description: Optional[str] = Field(None, max_length=2048)
    output_classification: Optional[str] = Field(None, max_length=128)

    request_classification: float
    is_public: bool = False

    class Config:
        orm_mode = True
