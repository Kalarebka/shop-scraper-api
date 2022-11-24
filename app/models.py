import re
from datetime import date, datetime, time
from enum import Enum
from typing import Generator, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, DESCENDING


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


class SortOrder(int, Enum):
    ascending = ASCENDING
    descending = DESCENDING


class SortBy(str, Enum):
    timestamp = "timestamp"
    book_title = "title"
    author = "author"


class OfferSearch(BaseModel):
    book_title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    from_date: Optional[date]
    to_date: Optional[date]
    available_only: bool = True
    sorted_by: SortBy = SortBy.timestamp
    sort_order: SortOrder = SortOrder.descending
    max_results: int = 0

    def create_filter_dict(self) -> dict:
        filter_params: dict = {}
        if self.book_title:
            filter_params["title"] = re.compile(self.book_title, re.IGNORECASE)

        if self.author:
            filter_params["author"] = re.compile(self.author, re.IGNORECASE)

        if self.isbn:
            filter_params["isbn"] = self.isbn.replace("-", "")

        if self.from_date:
            # Time() returns (0, 0) -> creates datetime with the date at midnight
            filter_params["timestamp"] = {
                "$gte": datetime.combine(self.from_date, time())
            }

        if self.to_date:
            filter_params["timestamp"] = {
                "$lte": datetime.combine(self.to_date, time())
            }

        if self.available_only:
            filter_params["available"] = self.available_only

        return filter_params


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
