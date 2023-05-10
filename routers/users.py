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

    if (existing_email := await _request.app.mongodb["user"].find_one({"email": _new_user["email"]}) is not None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {_new_user['email']} already exists")

    if (existing_username := await _request.app.mongodb["users"].find_one({"username": _new_user["username"]}) is not None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with username {_new_user['username']} already exists")

    user = await _request.app.mongodb["user"].insert_one(_new_user)
    created_user = await _request.app.mongodb["user"].find_one({"_id": user.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@users_router.post("/login", response_description="User Login")
async def login(_request: Request, _login_user: LoginBase = Body(...)) -> str:
    """The login endpoint for the user

    Args:
        _request (Request): The request object
        _login_user (LoginBase, optional): The login data. Defaults to Body(...).

    Raises:
        HTTPException: An exception thrown if the user is not found or has invalid credentials

    Returns:
        str: The response
    """
    _user = await _request.app.mongodb["user"].find_one({"email": _login_user.email})

    if (_user is None) or (not auth_handler.verify_password(_login_user.password, _user["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    token = auth_handler.encode_token(_user["_id"])
    response = JSONResponse(content={"token": token})
    return response


@users_router.get("/me", response_description="Logged in User Data")
async def me(_request: Request, _user_id: Depends(auth_handler.auth_wrapper)):
    """Returned information on the currently logged in user

    Args:
        _request (Request): The request object
        _user_id (Depends): The id of the logged in user

    Returns:
        _type_: A response in JSON format
    """
    _current_user = await _request.app.mongodb["users"].find_one({"_id": _user_id})
    _result = _current_user(**_current_user).dict()
    _result["id"] = _user_id

    return JSONResponse(status_code=status.HTTP_200_OK, content=_result)
