from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime
from typing import Optional

from database import get_db
from chat.manager import manager
from chat.schemas import UserMessage, ConnectionMessage, SystemMessage, AdminMessage
from auth.service import AuthService

class WebSocketChat:
    
    def __init__(self):
        self.DEFAULT_ROOM_ID = 1
        self.SUPPORT_ROOM_ID = 1  # ID комнаты поддержки
    
    async def authenticate_user(self, token: str, db: Session) -> dict:
        auth_service = AuthService(db)
        
        email = auth_service.verify_token(token, "access")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        from users.services import UserService
        user_service = UserService(db)
        db_user = user_service.repository.get_by_email(email)
        
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "is_admin": db_user.is_admin,
            "is_active": db_user.is_active
        }
    
    async def websocket_endpoint(
        self,
        websocket: WebSocket,
        token: Optional[str] = None,
        db: Session = None
    ):
        if not token:
            await websocket.close(code=1008, reason="Authentication token required")
            return
        
        if db is None:
            db = next(get_db())
        
        try:
            user = await self.authenticate_user(token, db)
            
            await websocket.accept()
            
            connection_id = None
            try:
                connection_id = await manager.connect(
                    websocket=websocket,
                    room_id=self.SUPPORT_ROOM_ID,
                    user_id=user["id"],
                    user_name=user["full_name"],
                    user_email=user["email"],
                    is_admin=user["is_admin"]
                )
                
                online_count = manager.get_online_count(self.SUPPORT_ROOM_ID)
                online_admins = manager.get_online_admins(self.SUPPORT_ROOM_ID)
                
                # Отправляем уведомление о подключении
                connection_msg = ConnectionMessage(
                    user_id=user["id"],
                    user_name=user["full_name"],
                    action="connected",
                    online_count=online_count
                )
                
                await manager.broadcast(
                    room_id=self.SUPPORT_ROOM_ID,
                    message=connection_msg.model_dump_json(),
                    exclude_connection_ids={connection_id}
                )
                
                # Приветственное сообщение
                if user["is_admin"]:
                    welcome_msg = SystemMessage(
                        message=f"Администратор {user['full_name']} в сети. Онлайн пользователей: {online_count}"
                    )
                else:
                    welcome_msg = SystemMessage(
                        message=f"Добро пожаловать в чат поддержки, {user['full_name']}! Администраторов онлайн: {len(online_admins)}"
                    )
                
                await manager.send_personal_message(
                    welcome_msg.model_dump_json(),
                    websocket
                )
                
                # Если пользователь - отправляем список админов
                if not user["is_admin"] and online_admins:
                    admins_list = ", ".join([admin["user_name"] for admin in online_admins])
                    info_msg = SystemMessage(
                        message=f"Доступные администраторы: {admins_list}"
                    )
                    await manager.send_personal_message(
                        info_msg.model_dump_json(),
                        websocket
                    )
                
                # История сообщений
                history = await self.get_message_history(db, self.SUPPORT_ROOM_ID, limit=50)
                if history:
                    await manager.send_personal_message(
                        json.dumps(history),
                        websocket
                    )
                
                # Основной цикл обработки сообщений
                while True:
                    data = await websocket.receive_text()
                    
                    try:
                        message_text = data.strip()
                        
                        if message_text:
                            # Проверяем специальные команды
                            if message_text.startswith("/"):
                                await self.handle_command(
                                    message_text, 
                                    user, 
                                    websocket, 
                                    connection_id, 
                                    db
                                )
                            else:
                                await self.handle_message(
                                    message_text, 
                                    user, 
                                    websocket, 
                                    connection_id, 
                                    db
                                )
                    
                    except Exception as e:
                        import logging
                        logging.error(f"Error processing message: {e}")
                        error_msg = SystemMessage(
                            message="Ошибка обработки сообщения"
                        )
                        await manager.send_personal_message(
                            error_msg.model_dump_json(),
                            websocket
                        )
            
            except WebSocketDisconnect:
                pass
            
            except Exception as e:
                import logging
                logging.error(f"WebSocket error: {e}")
            
            finally:
                if connection_id:
                    manager.disconnect(connection_id)
                    
                    online_count = manager.get_online_count(self.SUPPORT_ROOM_ID)
                    disconnect_msg = ConnectionMessage(
                        user_id=user["id"],
                        user_name=user["full_name"],
                        action="disconnected",
                        online_count=online_count
                    )
                    
                    await manager.broadcast(
                        room_id=self.SUPPORT_ROOM_ID,
                        message=disconnect_msg.model_dump_json()
                    )
        
        except HTTPException as e:
            await websocket.close(code=e.status_code, reason=e.detail)
        
        except Exception as e:
            await websocket.close(code=1008, reason="Internal server error")
        
        finally:
            if db is not None:
                db.close()
    
    async def handle_message(self, message_text: str, user: dict, websocket: WebSocket, connection_id: str, db: Session):
        """Обработка обычного сообщения"""
        
        # Сохраняем в БД
        saved_message = await self.save_message(
            db=db,
            user_id=user["id"],
            room_id=self.SUPPORT_ROOM_ID,
            message=message_text,
            is_admin_message=user["is_admin"]
        )
        
        if user["is_admin"]:
            if message_text.startswith("@") and " " in message_text:
                # Формат: "@username сообщение"
                parts = message_text.split(" ", 1)
                target_username = parts[0][1:]
                actual_message = parts[1]

                online_users = manager.get_online_users(self.SUPPORT_ROOM_ID)
                target_user = None
                
                for online_user in online_users:
                    if online_user["user_name"] == target_username:
                        target_user = online_user
                        break
                
                if target_user:
                    user_msg = UserMessage(
                        user_id=user["id"],
                        user_name=user["full_name"],
                        user_email=user["email"],
                        message=actual_message,
                        room_id=self.SUPPORT_ROOM_ID,
                        is_admin=True,
                        target_user_id=target_user["user_id"]
                    )
                    
                    await manager.send_to_user(
                        user_id=target_user["user_id"],
                        room_id=self.SUPPORT_ROOM_ID,
                        message=user_msg.model_dump_json()
                    )
                    await manager.send_personal_message(
                        user_msg.model_dump_json(),
                        websocket
                    )
                else:
                    user_msg = UserMessage(
                        user_id=user["id"],
                        user_name=user["full_name"],
                        user_email=user["email"],
                        message=message_text,
                        room_id=self.SUPPORT_ROOM_ID,
                        is_admin=True
                    )
                    
                    await manager.broadcast_to_users(
                        room_id=self.SUPPORT_ROOM_ID,
                        message=user_msg.model_dump_json()
                    )
            else:
                user_msg = UserMessage(
                    user_id=user["id"],
                    user_name=user["full_name"],
                    user_email=user["email"],
                    message=message_text,
                    room_id=self.SUPPORT_ROOM_ID,
                    is_admin=True
                )
                
                await manager.broadcast_to_users(
                    room_id=self.SUPPORT_ROOM_ID,
                    message=user_msg.model_dump_json()
                )
        else:
            user_msg = UserMessage(
                user_id=user["id"],
                user_name=user["full_name"],
                user_email=user["email"],
                message=message_text,
                room_id=self.SUPPORT_ROOM_ID,
                is_admin=False
            )
            
            await manager.broadcast_to_admins(
                room_id=self.SUPPORT_ROOM_ID,
                message=user_msg.model_dump_json()
            )
    
    async def handle_command(self, command: str, user: dict, websocket: WebSocket, connection_id: str, db: Session):
        """Обработка команд"""
        if command == "/users":
            # Показать онлайн пользователей
            online_users = manager.get_online_users(self.SUPPORT_ROOM_ID)
            users_list = "\n".join([f"{u['user_name']} ({'админ' if u.get('is_admin') else 'пользователь'})" 
                                   for u in online_users])
            
            response = SystemMessage(
                message=f"Онлайн пользователи:\n{users_list}"
            )
            await manager.send_personal_message(
                response.model_dump_json(),
                websocket
            )
        
        elif command == "/admins" and user["is_admin"]:
            online_admins = manager.get_online_admins(self.SUPPORT_ROOM_ID)
            admins_list = "\n".join([f"{a['user_name']}" for a in online_admins])
            
            response = SystemMessage(
                message=f"Онлайн администраторы:\n{admins_list}"
            )
            await manager.send_personal_message(
                response.model_dump_json(),
                websocket
            )
        
        elif command.startswith("/broadcast ") and user["is_admin"]:
            message = command[10:]
            
            user_msg = UserMessage(
                user_id=user["id"],
                user_name=user["full_name"],
                user_email=user["email"],
                message=message,
                room_id=self.SUPPORT_ROOM_ID,
                is_admin=True,
                is_broadcast=True
            )
            
            await manager.broadcast_to_users(
                room_id=self.SUPPORT_ROOM_ID,
                message=user_msg.model_dump_json()
            )
            
            await self.save_message(
                db=db,
                user_id=user["id"],
                room_id=self.SUPPORT_ROOM_ID,
                message=message,
                is_admin_message=True,
                is_broadcast=True
            )
        
        else:
            response = SystemMessage(
                message="Неизвестная команда. Доступные команды:\n/users - список онлайн\nДля админов: /admins, /broadcast сообщение"
            )
            await manager.send_personal_message(
                response.model_dump_json(),
                websocket
            )
    
    async def save_message(self, db: Session, user_id: int, room_id: int, message: str, 
                          is_admin_message: bool = False, is_broadcast: bool = False):
        from chat.models import ChatMessage
        
        try:
            chat_message = ChatMessage(
                room_id=room_id,
                user_id=user_id,
                message=message,
                is_read=False
            )
            
            db.add(chat_message)
            db.commit()
            db.refresh(chat_message)
            
            return chat_message
        
        except Exception as e:
            db.rollback()
            import logging
            logging.error(f"Error saving message to DB: {e}")
            return None
    
    async def get_message_history(self, db: Session, room_id: int, limit: int = 50):
        from chat.models import ChatMessage
        from users.models import User
        
        try:
            messages = db.query(ChatMessage, User)\
                .join(User, ChatMessage.user_id == User.id)\
                .filter(ChatMessage.room_id == room_id)\
                .order_by(ChatMessage.created_at.desc())\
                .limit(limit)\
                .all()
            
            history = []
            for chat_message, user in messages:
                history.append({
                    "id": chat_message.id,
                    "user_id": user.id,
                    "user_name": user.full_name,
                    "user_email": user.email,
                    "is_admin": user.is_admin,
                    "message": chat_message.message,
                    "created_at": chat_message.created_at.isoformat(),
                    "room_id": chat_message.room_id
                })
            
            return list(reversed(history))
        
        except Exception as e:
            import logging
            logging.error(f"Error getting message history: {e}")
            return []

websocket_chat = WebSocketChat()