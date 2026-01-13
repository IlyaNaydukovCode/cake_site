from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth.service import get_current_user
from users import schemas as user_schemas
from .user_services import AdminUserService
from . import schemas

router = APIRouter()

async def get_current_admin(current_user: user_schemas.UserResponse = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user

# УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ (АДМИН)

@router.get("/users", response_model=List[user_schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Получить всех пользователей (только для админов)"""
    admin_user_service = AdminUserService(db)
    return admin_user_service.get_all_users()

@router.post("/users/{user_id}/make-admin")
def make_user_admin(
    user_id: int,
    make_admin_data: schemas.MakeAdminRequest,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Назначить/снять права администратора с пользователя"""
    admin_user_service = AdminUserService(db)
    updated_user = admin_user_service.make_admin(user_id, make_admin_data.is_admin)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    action = "назначен администратором" if make_admin_data.is_admin else "лишен прав администратора"
    return {"message": f"User {updated_user.email} {action}"}