from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import schemas, service
from database import get_db
from auth.service import AuthService, get_auth_service
import re

router = APIRouter()


def validate_email(email: str) -> str:
    if not email:
        raise ValueError("Email is required")
    
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
    
    return email.lower()


@router.post("/register", response_model=schemas.TokenResponse)
def register(
    user_data: schemas.UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)
):
    from users.services import UserService
    user_service = UserService(db)
    
    try:
        user = user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    access_token, refresh_token = auth_service.create_tokens(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=schemas.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)
):
    try:
        email = validate_email(form_data.username)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    password = form_data.password
    if not password or len(password.strip()) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    from users.services import UserService
    user_service = UserService(db)
    user = user_service.authenticate_user(email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token, refresh_token = auth_service.create_tokens(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_tokens(
    refresh_data: schemas.RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    if not refresh_data.refresh_token or not refresh_data.refresh_token.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    tokens = auth_service.refresh_tokens(refresh_data.refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token, refresh_token = tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }