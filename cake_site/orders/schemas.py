from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional, List
from .models import OrderStatus, DeliveryType

class OrderBase(BaseModel):
    delivery_type: DeliveryType
    delivery_address: Optional[str] = None
    delivery_date: Optional[datetime] = None
    customer_notes: Optional[str] = None
    quantity: int = 1

class OrderCreate(OrderBase):
    cake_id: Optional[int] = Field(None, ge=1)  # Используем Field с ge=1
    custom_cake_id: Optional[int] = Field(None, ge=1)  # Используем Field с ge=1

    # Валидатор для проверки, что указан только один тип торта
    @model_validator(mode='after')
    def check_cake_or_custom_cake(self):
        if self.cake_id is not None and self.custom_cake_id is not None:
            raise ValueError('Укажите либо cake_id, либо custom_cake_id, но не оба')
        if self.cake_id is None and self.custom_cake_id is None:
            raise ValueError('Укажите либо cake_id, либо custom_cake_id')
        return self

class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    status: OrderStatus
    total_amount: float
    cake: Optional[dict] = None
    custom_cake: Optional[dict] = None

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    payment_method: str
    amount: float

class PaymentResponse(PaymentBase):
    id: int
    order_id: int
    payment_date: datetime
    payment_status: str
    transaction_id: Optional[str] = None

    class Config:
        from_attributes = True
