# cake_site/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Используем переменные окружения Docker
    database_url: str = "postgresql://cake_user:password@db:5432/cake_site"
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    
    # Docker-специфичные настройки
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()