from fastapi import APIRouter, Depends, HTTPException, status, Response
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
async def update_user(updated_details: UserDetails, response: Response, user: User = Depends(get_current_user)):
    try:
        if not updated_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No updated details provided"
            )
        
        updated_data = updated_details.model_dump(exclude_unset=True)
        print(updated_data)

        if 'password' in updated_data:
            updated_data['password'] = get_hashed_password(updated_data['password'])

        updated_user = users.find_one_and_update({'_id': ObjectId(user.id)}, {"$set": updated_data}, return_document=True)
        print(updated_user)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found after update"
            )

        if 'password' in updated_data:
            new_access_token = create_access_token(subject=str(updated_user['_id']))
            response.set_cookie(
                key="access_token",
                value=f"Bearer {new_access_token}",
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=1800
            )

        updated_user['_id'] = str(updated_user['_id'])
        return UserDetails(**updated_user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
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
