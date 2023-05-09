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
    """Class handles authorization"""
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ.get("SECRET_KEY")

    def get_password_hash(self, _password: str) -> str:
        """Returns the hashed password"""
        return self.pwd_context.hash(_password)

    def verify_password(self, _plain_password: str, _hashed_password: str) -> bool:
        """Verifies the password"""
        return self.pwd_context.verify(_plain_password, _hashed_password)

    def encode_token(self, _user_id):
        """The function that encodes the token.

        It takes the user id as a parameter and returns the token.

        Returns:
            str: The token.
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=35),
            "iat": datetime.utcnow(),
            "sub":  _user_id
        }

        return jwt.encode(
            payload,
            self.secret,
            algorithm="HS256"
        )
