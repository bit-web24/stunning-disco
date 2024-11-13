from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from app.auth.deps import create_access_token, get_current_user
from app.auth.password import get_hashed_password
from app.models.user import User, UserDetails
from app.database import users
from bson.objectid import ObjectId

router = APIRouter()

@router.get("/", response_model=UserDetails)
async def get_user(user: User = Depends(get_current_user)):
    try:
        return users.find_one({'_id': ObjectId(user.id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data"
        )

@router.put("/", response_model=UserDetails)
async def update_user(
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    password: Optional[str] = Form(None),
    response: Response = None,
    user: User = Depends(get_current_user)
):
    try:
        updated_data = {}
        if first_name is not None:
            updated_data['first_name'] = first_name
        if email is not None:
            updated_data['email'] = str(email)
        if last_name is not None:
            updated_data['last_name'] = last_name
        if password is not None:
            updated_data['password'] = get_hashed_password(password)

        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No updated details provided"
            )

        updated_user = users.find_one_and_update(
            {'_id': ObjectId(user.id)}, 
            {"$set": updated_data}, 
            return_document=True
        )

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found after update"
            )

        if password is not None:
            new_access_token = create_access_token(subject=str(updated_user['_id']))
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=1800
            )

        updated_user['_id'] = str(updated_user['_id'])
        return UserDetails(**updated_user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error updating user: {str(e)}")  # For debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user data"
        )

@router.delete("/", status_code=204)
async def delete_user(response: Response, user: User = Depends(get_current_user)):
    try:
        delete_result = users.delete_one({'_id': ObjectId(user.id)})

        if delete_result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or already deleted"
            )
        
        response.delete_cookie(key="access_token")
        return {"detail": "User deleted and token cleared"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
