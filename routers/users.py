"""The Users router file"""
from enum import Enum
from typing import Optional

from bson import ObjectId
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field, validator

users_router = APIRouter(prefix="Users", tags=["Users"])
