from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.sql import func
from database import Base

class Cake(Base):
    __tablename__ = "cakes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    is_available = Column(Boolean, default=True)
    weight = Column(Float)
    ingredients = Column(Text)

class CakeLayer(Base):
    __tablename__ = "cake_layers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

class Cream(Base):
    __tablename__ = "creams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

class Filling(Base):
    __tablename__ = "fillings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

class Decoration(Base):
    __tablename__ = "decorations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)