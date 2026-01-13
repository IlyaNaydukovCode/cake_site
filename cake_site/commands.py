from typing import Dict, Callable

CHAT_COMMANDS = {
    "/users": {
        "description": "Показать онлайн пользователей",
        "admin_only": False
    },
    "/admins": {
        "description": "Показать онлайн администраторов",
        "admin_only": True
    },
    "/broadcast": {
        "description": "Отправить сообщение всем пользователям",
        "admin_only": True,
        "usage": "/broadcast ваше сообщение"
    },
    "/help": {
        "description": "Показать список команд",
        "admin_only": False
    }
}