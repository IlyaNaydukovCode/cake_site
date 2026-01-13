from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class CustomCake(Base):
    __tablename__ = "custom_cakes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)

    layers = Column(JSON)
    creams = Column(JSON)
    fillings = Column(JSON)
    decorations = Column(JSON)
    
    total_price = Column(Float, nullable=False)
    weight = Column(Float)
    description = Column(String)

    user = relationship("User", back_populates="custom_cakes")
    orders = relationship("Order", back_populates="custom_cake")