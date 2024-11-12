from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone
from typing import Union, Any, Optional
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(tz=timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(tz=timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt
