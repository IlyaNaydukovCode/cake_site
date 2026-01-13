from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, services
from database import get_db
from auth.service import get_current_user
from users.schemas import UserResponse  # ← ИМПОРТИРОВАТЬ ИЗ users.schemas

router = APIRouter()


@router.post("/", response_model=schemas.OrderResponse)
def create_order(
        order_data: schemas.OrderCreate,
        current_user: UserResponse = Depends(get_current_user),  # ← ИСПОЛЬЗОВАТЬ UserResponse
        db: Session = Depends(get_db)
):
    order_service = services.OrderService(db)
    return order_service.create_order(current_user.id, order_data)


@router.get("/my-orders", response_model=List[schemas.OrderResponse])
def get_my_orders(
        current_user: UserResponse = Depends(get_current_user),  # ← ИСПОЛЬЗОВАТЬ UserResponse
        db: Session = Depends(get_db)
):
    order_service = services.OrderService(db)
    return order_service.get_user_orders(current_user.id)


@router.post("/{order_id}/pay", response_model=schemas.PaymentResponse)
def process_payment(
        order_id: int,
        payment_data: schemas.PaymentBase,
        current_user: UserResponse = Depends(get_current_user),  # ← ИСПОЛЬЗОВАТЬ UserResponse
        db: Session = Depends(get_db)
):
    order_service = services.OrderService(db)

    # Проверяем, что заказ принадлежит пользователю
    order = order_service.order_repo.get_order_by_id(order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    return order_service.process_payment(order_id, payment_data)