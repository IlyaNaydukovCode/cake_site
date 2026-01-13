from . import repositories, schemas
from cakes.repositories import CakeRepository
from constructor.repositories import CustomCakeRepository
from sqlalchemy.orm import Session
from typing import List, Optional

class OrderService:
    def __init__(self, db: Session):
        self.order_repo = repositories.OrderRepository(db)
        self.payment_repo = repositories.PaymentRepository(db)
        self.cake_repo = CakeRepository(db)
        self.custom_cake_repo = CustomCakeRepository(db)

    def calculate_order_total(self, order_data: schemas.OrderCreate) -> float:
        total = 0
        
        # Проверяем cake_id (должно быть не None и больше 0)
        if order_data.cake_id and order_data.cake_id > 0:
            cake = self.cake_repo.get_cake_by_id(order_data.cake_id)
            if cake:
                total = cake.price * order_data.quantity
        # Проверяем custom_cake_id (должно быть не None и больше 0)
        elif order_data.custom_cake_id and order_data.custom_cake_id > 0:
            custom_cake = self.custom_cake_repo.get_by_id(order_data.custom_cake_id)
            if custom_cake:
                total = custom_cake.total_price * order_data.quantity
        
        return total

    def create_order(self, user_id: int, order_data: schemas.OrderCreate) -> schemas.OrderResponse:
        total_amount = self.calculate_order_total(order_data)
        
        # Преобразуем в словарь и обрабатываем None значения
        order_dict = order_data.model_dump()
        
        # Явно устанавливаем None для неиспользуемых полей
        if not order_data.cake_id or order_data.cake_id <= 0:
            order_dict["cake_id"] = None
        if not order_data.custom_cake_id or order_data.custom_cake_id <= 0:
            order_dict["custom_cake_id"] = None
        
        order_dict.update({
            "user_id": user_id,
            "total_amount": total_amount,
            "status": "pending"  # Добавляем начальный статус
        })
        
        db_order = self.order_repo.create_order(order_dict)
        
        # Преобразуем SQLAlchemy объект в словарь перед валидацией
        order_dict_for_response = {
            "id": db_order.id,
            "user_id": db_order.user_id,
            "order_date": db_order.order_date,
            "status": db_order.status,
            "total_amount": db_order.total_amount,
            "delivery_type": db_order.delivery_type,
            "delivery_address": db_order.delivery_address,
            "delivery_date": db_order.delivery_date,
            "customer_notes": db_order.customer_notes,
            "quantity": db_order.quantity,
        }
        
        # Преобразуем cake в словарь если он есть
        if db_order.cake:
            order_dict_for_response["cake"] = {
                "id": db_order.cake.id,
                "name": db_order.cake.name,
                "price": db_order.cake.price,
                "description": db_order.cake.description,
                "image_url": db_order.cake.image_url,
                "weight": db_order.cake.weight,
                "ingredients": db_order.cake.ingredients,
                "is_available": db_order.cake.is_available
            }
        
        # Преобразуем custom_cake в словарь если он есть
        if db_order.custom_cake:
            order_dict_for_response["custom_cake"] = {
                "id": db_order.custom_cake.id,
                "name": db_order.custom_cake.name,
                "total_price": db_order.custom_cake.total_price,
                "description": db_order.custom_cake.description,
                "layers": db_order.custom_cake.layers,
                "creams": db_order.custom_cake.creams,
                "filling": db_order.custom_cake.fillings,
                "decorations": db_order.custom_cake.decorations
            }
        
        return schemas.OrderResponse.model_validate(order_dict_for_response)

    def get_user_orders(self, user_id: int) -> List[schemas.OrderResponse]:
        orders = self.order_repo.get_user_orders(user_id)
        result = []
        
        for order in orders:
            # Преобразуем каждый заказ в словарь
            order_dict = {
                "id": order.id,
                "user_id": order.user_id,
                "order_date": order.order_date,
                "status": order.status,
                "total_amount": order.total_amount,
                "delivery_type": order.delivery_type,
                "delivery_address": order.delivery_address,
                "delivery_date": order.delivery_date,
                "customer_notes": order.customer_notes,
                "quantity": order.quantity,
            }
            
            if order.cake:
                order_dict["cake"] = {
                    "id": order.cake.id,
                    "name": order.cake.name,
                    "price": order.cake.price,
                    "description": order.cake.description,
                    "image_url": order.cake.image_url,
                    "weight": order.cake.weight,
                    "ingredients": order.cake.ingredients,
                    "is_available": order.cake.is_available
                }
            
            if order.custom_cake:
                order_dict["custom_cake"] = {
                    "id": order.custom_cake.id,
                    "name": order.custom_cake.name,
                    "total_price": order.custom_cake.total_price,
                    "description": order.custom_cake.description,
                    "layers": order.custom_cake.layers,
                    "creams": order.custom_cake.creams,
                    "filling": order.custom_cake.fillings,
                    "decorations": order.custom_cake.decorations
                }
            
            result.append(schemas.OrderResponse.model_validate(order_dict))
        
        return result

    def process_payment(self, order_id: int, payment_data: schemas.PaymentBase) -> schemas.PaymentResponse:
        payment_dict = payment_data.model_dump()
        payment_dict.update({
            "order_id": order_id,
            "payment_status": "completed",
            "transaction_id": f"txn_{order_id}_{payment_data.payment_method}"
        })
        
        db_payment = self.payment_repo.create_payment(payment_dict)
        
        self.order_repo.update_order_status(order_id, "confirmed")
        
        return schemas.PaymentResponse.model_validate(db_payment)