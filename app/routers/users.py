from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User
from app.db import db

router = APIRouter()
users = db.set_collection("users")

@router.get("/", response_model=List[User])
def get_users():
    return users.get_all()

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    user = users.get({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=201)
def create_user(user: User):
    users.insert(user.dict())
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: User):
    existing_user = users.get({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users.update(existing_user, user.dict())
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    existing_user = users.get({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users.delete(existing_user)

