from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Role
from app.schemas import TokenData
from app.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import joinedload
security = HTTPBearer()


SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 часа

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # Добавляем joinedload для role
    result = await db.execute(
        select(User)
        .where(User.id_user == token_data.user_id)
        .options(joinedload(User.role))
    )
    user = result.unique().scalar_one_or_none()  # unique() обязателен при joinedload
    if user is None or user.is_deleted:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def role_required(required_roles: list[str]):
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        result = current_user.role.role_name
        if result not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

# async def get_current_user_optional(
#     token: Optional[str] = Depends(oauth2_scheme_optional),  # своя OAuth2PasswordBearer с auto_error=False
#     db: AsyncSession = Depends(get_db)
# ) -> Optional[User]:
#     if not token:
#         return None
#     try:
#         return await get_current_user(token, db)
#     except HTTPException:
#         return None
roles = ["student", "author",  "moderator", "admin",]

# Для удобства
student_or_above = role_required(roles)
author_or_above = role_required(roles[1:])
moderator_or_above = role_required(roles[2:])
admin_or_above = role_required(roles[3:])