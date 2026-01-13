from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CakeComponent(BaseModel):
    id: int
    quantity: int

class CustomCakeCreate(BaseModel):
    name: Optional[str] = None
    layers: List[CakeComponent]
    creams: List[CakeComponent]
    fillings: List[CakeComponent]
    decorations: List[CakeComponent]

class CustomCakeResponse(BaseModel):
    id: int
    name: Optional[str]
    layers: List[Dict[str, Any]]
    creams: List[Dict[str, Any]]
    fillings: List[Dict[str, Any]]
    decorations: List[Dict[str, Any]]
    total_price: float
    weight: float
    description: Optional[str]

    class Config:
        from_attributes = True