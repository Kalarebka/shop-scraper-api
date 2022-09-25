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
    name: str
    timestamp: datetime = Field(...)
    shop_id: int
    price: float
    shipping: Optional[float]
    exact: bool = False
    available: bool = False
    url: str


class Product(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    query: str = Field(...)
    offers = List[Offer]
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Shop(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    type: str = Field(...)
    scraper: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
