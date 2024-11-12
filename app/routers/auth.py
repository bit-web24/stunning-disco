from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserAuth
from app.db import db
from app.auth.password import (
    get_hashed_password,
    create_access_token,
    # create_refresh_token,
    verify_password
)

router = APIRouter()
users = db.set_collection('users')

@router.post('/signup', summary="Create new user", response_model=User)
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get({'username' : form_data.username})
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = UserAuth(username=form_data.username, password=get_hashed_password(form_data.password))
    user = users.insert(user.dict())
    user['_id'] = str(user['_id'])
    return user

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get({'username' : form_data.username})
    
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the access token
    access_token = create_access_token(subject=user['_id'])
    
    # Set the token in a secure HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=1800  # Optional: max-age for cookie (in seconds)
    )

    # Optional: return a success message or user data
    return {"message": "Login successful"}

@router.get('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}
