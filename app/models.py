from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field, Optional

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
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    timestamp: datetime = Field(...)
    shop_id: int
    price: float
    shipping: Optional[float]
    exact: bool = False
    available: bool = False
    url: str


class ProductQuery(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    query: str = Field(...)
    num_results: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
