from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from database import get_db
from auth.service import get_current_user

router = APIRouter()

@router.get("/", response_model=schemas.UserResponse)
def get_current_user_info(
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return current_user

@router.put("/", response_model=schemas.UserResponse)
def update_user_info(
    user_update: schemas.UserUpdate,
    current_user: schemas.UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = services.UserService(db)
    
    updated_user = user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user