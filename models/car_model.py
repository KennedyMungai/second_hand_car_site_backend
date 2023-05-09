"""The model file for the car"""
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """The class that makes the object id

    Args:
        ObjectId (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, _v):
        """Validation method

        Args:
            v (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not ObjectId.is_valid(_v):
            raise ValueError("Invalid objectid")
        return ObjectId(_v)

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
    make: str = Field(..., min_length=1)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(..., gt=600, lt=8000)


class CarUpdate(MongoBaseModel):
    """Defined the car update class

    Args:
        MongoBaseModel (The Base model for the mongodb): Mongodb base model
    """
    price: Optional[int] = None


class CarDB(CarBase):
    """The car database model

    Args:
        CarBase (CarBase): The car base model
    """
    owner: str = Field(...)
