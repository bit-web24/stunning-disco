from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.auth.deps import get_current_user
from app.models.user import User
from app.database import users

router = APIRouter()

@router.get("/", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    try:
        user_dict = user.dict()
        user_dict['_id'] = user_dict.pop('id')
        return User(**user_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data"
        )

@router.put("/", response_model=User)
async def update_user(user: User = Depends(get_current_user), updated_details: User = None):
    try:
        if not updated_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No updated details provided"
            )
        
        users.update_one({'_id': user._id}, {"$set": updated_details.dict()})
        
        updated_user = users.find_one({'_id': user._id})
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found after update"
            )
        
        return User(**updated_user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user data"
        )

@router.delete("/", status_code=204)
async def delete_user(response: Response, user: User = Depends(get_current_user)):
    try:
        delete_result = users.delete_one({'_id': user._id})
        if delete_result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or already deleted"
            )
        
        response.delete_cookie(key="access_token")
        return {"detail": "User deleted and token cleared"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
