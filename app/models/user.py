from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username: str
    password: str


class UserAuth(BaseModel):
    username: str
    password: str
