from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from jose import jwt
from pydantic import ValidationError
from app.models.user import User
from app.models.token import TokenPayload
from app.db import db
from dotenv import load_dotenv

load_dotenv()

users = db.set_collection("users")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/token",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, os.environ.get('JWT_SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = users.get({'_id': token_data.sub})


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return User(**user)
