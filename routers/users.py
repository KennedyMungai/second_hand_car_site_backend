"""The Users router file"""
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth.authentication import AuthHandler
from models.user_model import CurrentUser, LoginBase, UserBase

users_router = APIRouter(prefix="Users", tags=["Users"])
auth_handler = AuthHandler()


@users_router.post("/register", response_description="User Registration")
async def register_user(_request: Request, _new_user: UserBase = Body(...)) -> UserBase:
    """An endpoint to register users

    Args:
        request (Request): Register Object
        _new_user (UserBase, optional): User Data. Defaults to Body(...).
    """
    _new_user.password = auth_handler.get_password_hash(_new_user.password)
    _new_user = jsonable_encoder(_new_user)
