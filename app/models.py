from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Optional

# from mongodb.com; convert bson ObjectIds to strings
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Offer(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", exclude=True)
    title: str = Field(...)
    author: str = Field(...)
    isbn: str
    timestamp: datetime = Field(...)
    shop: str = Field(...)
    price: float = Field(...)
    available: bool = False
    url: str = Field(...)
    query: str = Field(...)


class Query(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    query: str = Field(...)
    active: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateQuery(BaseModel):
    query: Optional[str]
    active: Optional[bool]

    class Config:
        arbitrary_types_allowed = True


class CreateQuery(BaseModel):
    query: str = Field(...)
    active: bool = True

    class Config:
        arbitrary_types_allowed = True
