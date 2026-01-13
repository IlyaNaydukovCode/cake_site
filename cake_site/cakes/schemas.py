from pydantic import BaseModel
from typing import Optional, List

class CakeBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    weight: Optional[float] = None
    ingredients: Optional[str] = None

class CakeCreate(CakeBase):
    pass

class CakeResponse(CakeBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True

class ComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_unit: float

class ComponentResponse(ComponentBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True

class CakeLayerResponse(ComponentResponse):
    pass

class CreamResponse(ComponentResponse):
    pass

class FillingResponse(ComponentResponse):
    pass

class DecorationResponse(ComponentResponse):
    pass