from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from auth.service import get_current_user
from users.schemas import UserResponse
from chat import schemas, manager
from chat.models import ChatRoom, ChatMessage
from chat.websocket import websocket_chat

router = APIRouter()

@router.websocket("/ws")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    token: str = Query(None)
):
    db = next(get_db())
    try:
        await websocket_chat.websocket_endpoint(websocket, token, db)
    finally:
        db.close()

@router.get("/rooms", response_model=List[schemas.RoomResponse])
async def get_chat_rooms(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    rooms = db.query(ChatRoom).filter(ChatRoom.is_active == True).all()
    
    result = []
    for room in rooms:
        room_dict = schemas.RoomResponse.model_validate(room)
        room_dict.message_count = db.query(ChatMessage)\
            .filter(ChatMessage.room_id == room.id)\
            .count()
        room_dict.online_count = manager.get_online_count(room.id)
        result.append(room_dict)
    
    return result

@router.get("/rooms/{room_id}/messages", response_model=List[schemas.MessageResponse])
async def get_room_messages(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    from users.models import User
    
    messages = db.query(ChatMessage, User)\
        .join(User, ChatMessage.user_id == User.id)\
        .filter(ChatMessage.room_id == room_id)\
        .order_by(ChatMessage.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    result = []
    for chat_message, user in messages:
        result.append(schemas.MessageResponse(
            id=chat_message.id,
            user_id=user.id,
            user_name=user.full_name,
            user_email=user.email,
            message=chat_message.message,
            created_at=chat_message.created_at,
            room_id=chat_message.room_id
        ))
    
    return list(reversed(result))

@router.get("/rooms/{room_id}/online", response_model=List[dict])
async def get_online_users(
    room_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return manager.get_online_users(room_id)

@router.post("/send", response_model=schemas.MessageResponse)
async def send_message(
    message_data: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    from chat.models import ChatMessage
    from chat.schemas import UserMessage
    
    chat_message = ChatMessage(
        room_id=message_data.room_id or 1,
        user_id=current_user.id,
        message=message_data.message
    )
    
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    user_msg = UserMessage(
        user_id=current_user.id,
        user_name=current_user.full_name,
        user_email=current_user.email,
        message=message_data.message,
        room_id=message_data.room_id or 1
    )
    
    await manager.broadcast(
        room_id=message_data.room_id or 1,
        message=user_msg.model_dump_json()
    )
    
    return schemas.MessageResponse(
        id=chat_message.id,
        user_id=current_user.id,
        user_name=current_user.full_name,
        user_email=current_user.email,
        message=message_data.message,
        created_at=chat_message.created_at,
        room_id=message_data.room_id or 1
    )