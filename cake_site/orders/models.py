from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class DeliveryType(str, enum.Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
    delivery_type = Column(SQLEnum(DeliveryType), nullable=False)
    delivery_address = Column(String)
    delivery_date = Column(DateTime(timezone=True))
    customer_notes = Column(String)
    
    # Для готовых тортов
    cake_id = Column(Integer, ForeignKey("cakes.id"))
    # Для кастомных тортов
    custom_cake_id = Column(Integer, ForeignKey("custom_cakes.id"))
    quantity = Column(Integer, default=1)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    cake = relationship("Cake")
    custom_cake = relationship("CustomCake")
    payments = relationship("Payment", back_populates="order")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_method = Column(String)  # card, cash, etc.
    payment_status = Column(String)  # pending, completed, failed
    transaction_id = Column(String)
    
    order = relationship("Order", back_populates="payments")