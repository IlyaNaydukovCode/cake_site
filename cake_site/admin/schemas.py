from pydantic import BaseModel
from typing import Optional, List
from users.schemas import UserResponse

# Схемы для управления пользователями
class MakeAdminRequest(BaseModel):
    is_admin: bool = True

class UserUpdateAdmin(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

class UserCreateAdmin(BaseModel):
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_admin: Optional[bool] = False

class UsersListResponse(BaseModel):
    users: List[UserResponse]
    total: int

# Схемы для тортов и компонентов
class CakeBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    weight: Optional[float] = None
    ingredients: Optional[str] = None

class CakeCreate(CakeBase):
    pass

class CakeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    weight: Optional[float] = None
    ingredients: Optional[str] = None
    is_available: Optional[bool] = None

class ComponentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_unit: float

class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_unit: Optional[float] = None
    is_available: Optional[bool] = None

class CakeLayerResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price_per_unit: float
    is_available: bool

    class Config:
        from_attributes = True

class CreamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price_per_unit: float
    is_available: bool

    class Config:
        from_attributes = True

class FillingResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price_per_unit: float
    is_available: bool

    class Config:
        from_attributes = True

class DecorationResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price_per_unit: float
    is_available: bool

    class Config:
        from_attributes = True

class AdminOrderStats(BaseModel):
    total_orders: int
    total_revenue: float
    orders_by_status: dict