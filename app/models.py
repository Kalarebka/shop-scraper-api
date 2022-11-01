from datetime import date, datetime
from typing import Generator, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


# from mongodb.com; convert bson ObjectIds to strings
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(type="string")


class Offer(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", exclude=True)
    title: str = Field(...)
    author: str = Field(...)
    isbn: Optional[str]
    timestamp: datetime = Field(...)
    shop: str = Field(...)
    price: float = Field(...)
    available: bool = False
    url: str = Field(...)
    query: str = Field(...)


class OfferSearch(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    from_date: Optional[date]
    to_date: Optional[date]
    available_only: bool = True
    sorted_by: str = "timestamp"
    reverse: bool = True
    max_results: int = 0


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
