from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_tokens(self, email: str) -> Tuple[str, str]:
        access_token = self._create_access_token(email)
        refresh_token = self._create_refresh_token(email)
        return access_token, refresh_token

    def _create_access_token(self, email: str, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = {"sub": email, "type": "access"}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    def _create_refresh_token(self, email: str) -> str:
        to_encode = {"sub": email, "type": "refresh"}
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            if payload.get("type") != token_type:
                return None
            email: str = payload.get("sub")
            return email
        except JWTError:
            return None

    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        email = self.verify_token(refresh_token, "refresh")
        if not email:
            return None
        return self.create_tokens(email)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    email = auth_service.verify_token(token, "access")
    if not email:
        raise credentials_exception
    
    # Импортируем здесь, чтобы избежать циклической зависимости
    from users.services import UserService
    user_service = UserService(db)
    db_user = user_service.repository.get_by_email(email)
    
    if db_user is None:
        raise credentials_exception
    
    from users.schemas import UserResponse
    return UserResponse.model_validate(db_user)


async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
