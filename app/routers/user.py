from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user
from app.models.user import User
from app.db import db

router = APIRouter()
users = db.set_collection("users")

@router.get("/", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user.dict()

@router.put("/", response_model=User)
async def update_user(user: User = Depends(get_current_user), updated_details: User = None):
    users.update(user.dict(), updated_details)
    return users.get({'_id': user._id})

@router.delete("/", status_code=204)
async def delete_user(user: User = Depends(get_current_user)):
    users.delete(user.dict())

