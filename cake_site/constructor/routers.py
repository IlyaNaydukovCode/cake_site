from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from database import get_db
from auth.service import get_current_user
from users.schemas import UserResponse  # ← ДОБАВИТЬ ИМПОРТ

router = APIRouter()

@router.post("/create", response_model=schemas.CustomCakeResponse)
def create_custom_cake(
    cake_data: schemas.CustomCakeCreate,
    current_user: UserResponse = Depends(get_current_user),  # ← ИСПОЛЬЗОВАТЬ UserResponse
    db: Session = Depends(get_db)
):
    constructor_service = services.ConstructorService(db)
    return constructor_service.create_custom_cake(current_user.id, cake_data)

@router.post("/calculate-price")
def calculate_cake_price(
    cake_data: schemas.CustomCakeCreate,
    db: Session = Depends(get_db)
):
    constructor_service = services.ConstructorService(db)
    return constructor_service.calculate_cake_price(cake_data)