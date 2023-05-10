"""The Users router file"""
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth.authentication import AuthHandler
from models.user_model import CurrentUser, LoginBase, UserBase

users_router = APIRouter(prefix="Users", tags=["Users"])
auth_handler = AuthHandler()
