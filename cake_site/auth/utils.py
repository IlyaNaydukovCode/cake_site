from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if len(plain_password.encode('utf-8')) > 72:
        return False
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password is too long. Maximum length is 72 bytes (approximately 72 characters)")
    return pwd_context.hash(password)
