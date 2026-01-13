from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from typing import List, Optional, Dict

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[models.Order]:
        return self.db.query(models.Order)\
            .order_by(models.Order.order_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_order_by_id(self, order_id: int) -> Optional[models.Order]:
        return self.db.query(models.Order).filter(models.Order.id == order_id).first()

    def get_user_orders(self, user_id: int) -> List[models.Order]:
        return self.db.query(models.Order)\
            .filter(models.Order.user_id == user_id)\
            .order_by(models.Order.order_date.desc())\
            .all()

    def create_order(self, order_data: dict) -> models.Order:
        db_order = models.Order(**order_data)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def update_order_status(self, order_id: int, status: str) -> Optional[models.Order]:
        db_order = self.get_order_by_id(order_id)
        if db_order:
            db_order.status = models.OrderStatus(status)
            self.db.commit()
            self.db.refresh(db_order)
        return db_order

    # Методы для статистики
    def get_total_orders_count(self) -> int:
        return self.db.query(func.count(models.Order.id)).scalar()

    def get_total_revenue(self) -> float:
        result = self.db.query(func.sum(models.Order.total_amount)).scalar()
        return float(result) if result else 0.0

    def get_orders_by_status(self) -> Dict[str, int]:
        from sqlalchemy import func
        status_counts = self.db.query(
            models.Order.status, 
            func.count(models.Order.id)
        ).group_by(models.Order.status).all()
        
        return {status.value: count for status, count in status_counts}

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment_data: dict) -> models.Payment:
        db_payment = models.Payment(**payment_data)
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def get_payment_by_order_id(self, order_id: int) -> Optional[models.Payment]:
        return self.db.query(models.Payment).filter(models.Payment.order_id == order_id).first()