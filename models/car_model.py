"""The model file for the car"""
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


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


class MongoBaseModel(BaseModel):
    """The Base Model using the mongo if

    Args:
        BaseModel (Pydantic): A pydantic base model
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        """The configuration subclass for MongoBaseModel
        """
        json_encoders = {ObjectId: str}


class CarBase(MongoBaseModel):
    """The base model for the car

    Args:
        MongoBaseModel (MongoBaseModel): The base model for the mongo
    """
    brand: str = Field(..., min_length=3)
    make: str = Field(..., min_length=3)
    year: int = Field(...)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)


class CarUpdate(MongoBaseModel):
    """Defined the car update class

    Args:
        MongoBaseModel (The Base model for the mongodb): Mongodb base model
    """
    price: Optional[int] = None
