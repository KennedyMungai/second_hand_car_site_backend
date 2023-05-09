"""The file with the authentication logic"""
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


class Authorization():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ.get("SECRET_KEY")
