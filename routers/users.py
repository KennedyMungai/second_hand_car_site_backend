"""The Users router file"""
from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.user_model import UserBase, LoginBase, CurrentUser
from auth.authentication import AuthHandler

users_router = APIRouter(prefix="Users", tags=["Users"])
auth_handler = AuthHandler()
