from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    password: str
    
    class Config:
        json_encoders = {
            ObjectId: str
        }


class UserAuth(BaseModel):
    username: str
    password: str

class UserDetails(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
