"""Created the User model file"""
from enum import Enum
from typing import Optional

from bson import ObjectId
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field, validator


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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Role(str, Enum):
    """A class that defines the different user roles

    Args:
        str (_type_): Strings
        Enum (_type_): Enums
    """
    SALESPERSON = "SALESPERSON"
    ADMIN = "ADMIN"


class UserBase(MongoBaseModel):
    """The base template for user data

    Args:
        MongoBaseModel (Mongo data): The base mongo data
    """
    username: str = Field(..., min_length=3, max_length=15)
    email: str = Field(...)
    password: str = Field(...)
    role: Role


@validator("email")
def valid_email(cls, v):
    """Wrote a simple email validator class

    Args:
        v (_type_): _description_

    Raises:
        EmailNotValidError: Email not valid exception

    Returns:
        email: The valid email
    """
    try:
        email = validate_email(v).email
        return email
    except:
        raise EmailNotValidError()
