import os
from typing import Union, Any, Optional
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from app.models.user import User
from app.models.token import TokenPayload
from app.database import users
from dotenv import load_dotenv

load_dotenv()

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(tz=timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
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
    
    user = users.find_one({'_id': ObjectId(token_data.sub)})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    user['_id'] = str(user['_id'])
    return User(**user)
