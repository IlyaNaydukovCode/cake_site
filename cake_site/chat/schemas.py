# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class MessageBase(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    room_id: Optional[int] = Field(1, description="ID комнаты чата")

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    is_admin: bool
    message: str
    created_at: datetime
    room_id: int
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    is_active: bool
    created_at: datetime
    message_count: Optional[int] = 0
    online_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class SystemMessage(BaseModel):
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class UserMessage(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    message: str
    is_admin: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    room_id: int = 1
    target_user_id: Optional[int] = None
    is_broadcast: bool = False

class ConnectionMessage(BaseModel):
    user_id: int
    user_name: str
    is_admin: bool = False
    action: str  # "connected" or "disconnected"
    online_count: int
    timestamp: datetime = Field(default_factory=datetime.now)

class AdminMessage(BaseModel):
    """Сообщение от администратора"""
    user_id: int
    user_name: str
    user_email: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    room_id: int = 1
    target_user_id: Optional[int] = None
    is_broadcast: bool = False