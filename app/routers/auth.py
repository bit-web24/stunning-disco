from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserAuth
from app.models.token import TokenSchema
from app.database import users
from app.auth.password import (
    get_hashed_password,
    verify_password
)
from bson.objectid import ObjectId
from app.auth.deps import create_access_token

router = APIRouter()

@router.post('/signup', summary="Create new user", response_model=User)
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({'username' : form_data.username})
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )
    user_auth = UserAuth(username=form_data.username, password=get_hashed_password(form_data.password))
    user = users.insert_one(user_auth.model_dump())
    user = users.find_one({'_id': ObjectId(user.inserted_id)})
    user['_id'] = str(user['_id'])
    return User(**user)

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({'username' : form_data.username})
    
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=str(user['_id']))
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=1800
    )

    return {"message": "Login successful"}

@router.get('/logout')
async def logout(response: Response):
    try:
        response.delete_cookie(key="access_token")
        return {"message": "Logout successful"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging out"
        )


@router.post('/token', summary="get access token", response_model=TokenSchema)
async def get_token(request: Request):
    access_token = request.cookies.get('access_token')
    return {"access_token": access_token, "token_type": "bearer"}
