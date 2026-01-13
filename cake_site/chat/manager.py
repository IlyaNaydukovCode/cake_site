# manager.py
import asyncio
from typing import Dict, Set, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:    
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, Set]] = {}
        self.connection_info: Dict[str, Dict] = {}
        
    async def connect(self, websocket, room_id: int, user_id: int, user_name: str, user_email: str, is_admin: bool = False):
        connection_id = str(id(websocket))

        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}

        if user_id not in self.active_connections[room_id]:
            self.active_connections[room_id][user_id] = set()
        
        self.active_connections[room_id][user_id].add(connection_id)
        self.connection_info[connection_id] = {
            "user_id": user_id,
            "room_id": room_id,
            "user_name": user_name,
            "user_email": user_email,
            "is_admin": is_admin,
            "websocket": websocket
        }
        
        logger.info(f"User {user_name} (admin: {is_admin}) connected to room {room_id}")
        return connection_id
    
    def disconnect(self, connection_id: str):
        if connection_id in self.connection_info:
            info = self.connection_info[connection_id]
            room_id = info["room_id"]
            user_id = info["user_id"]
            user_name = info["user_name"]
            
            if room_id in self.active_connections:
                if user_id in self.active_connections[room_id]:
                    self.active_connections[room_id][user_id].discard(connection_id)

                    if not self.active_connections[room_id][user_id]:
                        del self.active_connections[room_id][user_id]

                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]

            del self.connection_info[connection_id]
            
            logger.info(f"User {user_name} disconnected")
    
    def get_online_users(self, room_id: int) -> List[Dict]:
        if room_id not in self.active_connections:
            return []
        
        online_users = []
        for user_id, connections in self.active_connections[room_id].items():
            if connections:
                connection_id = next(iter(connections))
                if connection_id in self.connection_info:
                    info = self.connection_info[connection_id]
                    online_users.append({
                        "user_id": user_id,
                        "user_name": info["user_name"],
                        "user_email": info["user_email"],
                        "is_admin": info["is_admin"]
                    })
        
        return online_users
    
    def get_online_admins(self, room_id: int) -> List[Dict]:
        if room_id not in self.active_connections:
            return []
        
        admins = []
        for user_id, connections in self.active_connections[room_id].items():
            if connections:
                connection_id = next(iter(connections))
                if connection_id in self.connection_info and self.connection_info[connection_id]["is_admin"]:
                    info = self.connection_info[connection_id]
                    admins.append({
                        "user_id": user_id,
                        "user_name": info["user_name"],
                        "user_email": info["user_email"]
                    })
        
        return admins
    
    def get_online_users_by_type(self, room_id: int, is_admin: bool) -> List[Dict]:
        if room_id not in self.active_connections:
            return []
        
        users = []
        for user_id, connections in self.active_connections[room_id].items():
            if connections:
                connection_id = next(iter(connections))
                if connection_id in self.connection_info and self.connection_info[connection_id]["is_admin"] == is_admin:
                    info = self.connection_info[connection_id]
                    users.append({
                        "user_id": user_id,
                        "user_name": info["user_name"],
                        "user_email": info["user_email"]
                    })
        
        return users
    
    def get_online_count(self, room_id: int) -> int:
        if room_id not in self.active_connections:
            return 0
        
        return len(self.active_connections[room_id])
    
    async def send_personal_message(self, message: str, websocket):
        await websocket.send_text(message)
    
    async def broadcast(self, room_id: int, message: str, exclude_connection_ids: Set[str] = None):
        if room_id not in self.active_connections:
            return
        
        if exclude_connection_ids is None:
            exclude_connection_ids = set()
        
        tasks = []
        for user_id, connections in self.active_connections[room_id].items():
            for connection_id in connections:
                if connection_id not in exclude_connection_ids:
                    if connection_id in self.connection_info:
                        websocket = self.connection_info[connection_id]["websocket"]
                        try:
                            tasks.append(websocket.send_text(message))
                        except Exception as e:
                            logger.error(f"Error sending message: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_to_user(self, user_id: int, room_id: int, message: str):
        if room_id not in self.active_connections:
            return
        
        if user_id not in self.active_connections[room_id]:
            return
        
        tasks = []
        for connection_id in self.active_connections[room_id][user_id]:
            if connection_id in self.connection_info:
                websocket = self.connection_info[connection_id]["websocket"]
                try:
                    tasks.append(websocket.send_text(message))
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_to_all_admins(self, room_id: int, message: str, exclude_user_ids: Set[int] = None):
        if room_id not in self.active_connections:
            return
        
        if exclude_user_ids is None:
            exclude_user_ids = set()
        
        tasks = []
        for user_id, connections in self.active_connections[room_id].items():
            if user_id in exclude_user_ids:
                continue
                
            if connections:
                connection_id = next(iter(connections))
                if connection_id in self.connection_info and self.connection_info[connection_id]["is_admin"]:
                    for connection_id in connections:
                        if connection_id in self.connection_info:
                            websocket = self.connection_info[connection_id]["websocket"]
                            try:
                                tasks.append(websocket.send_text(message))
                            except Exception as e:
                                logger.error(f"Error sending message to admin {user_id}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_to_all_users(self, room_id: int, message: str, exclude_user_ids: Set[int] = None):
        if room_id not in self.active_connections:
            return
        
        if exclude_user_ids is None:
            exclude_user_ids = set()
        
        tasks = []
        for user_id, connections in self.active_connections[room_id].items():
            if user_id in exclude_user_ids:
                continue
                
            if connections:
                connection_id = next(iter(connections))
                if connection_id in self.connection_info and not self.connection_info[connection_id]["is_admin"]:
                    for connection_id in connections:
                        if connection_id in self.connection_info:
                            websocket = self.connection_info[connection_id]["websocket"]
                            try:
                                tasks.append(websocket.send_text(message))
                            except Exception as e:
                                logger.error(f"Error sending message to user {user_id}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def broadcast_to_admins(self, room_id: int, message: str):
        await self.send_to_all_admins(room_id, message)
    
    async def broadcast_to_users(self, room_id: int, message: str):
        await self.send_to_all_users(room_id, message)

manager = ConnectionManager()