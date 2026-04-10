"""
Аутентификация: хэширование пароля (argon2), выпуск и проверка JWT.

Токен кладёт в payload поле sub = email пользователя (совместимо с OAuth2 password flow).
"""

import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from config import app_settings, database_engine_async
from models.main_app_user_model import AppUser
from utils.internal_workers.database_worker import DatabaseWorkerAsync

logger = logging.getLogger("app.services.auth")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
database_worker = DatabaseWorkerAsync(database_engine_async)


class AuthNamespace:
    """Статические методы для паролей, JWT и входа по форме OAuth2."""

    @staticmethod
    def _get_password_hash(password) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, password_hash: str) -> bool:
        return pwd_context.verify(plain_password, password_hash)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now() + (
            expires_delta if expires_delta else timedelta(minutes=15)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    async def _authenticate_user(email: str, raw_password: str) -> AppUser:
        user: AppUser = await database_worker.custom_orm_select(
            cls_from=AppUser, where_params=[AppUser.email == email], return_unpacked=True
        )
        if not isinstance(user, AppUser):
            raise HTTPException(status_code=401, detail="User not found")
        if not AuthNamespace._verify_password(
            plain_password=raw_password, password_hash=user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Wrong password")
        return user

    @staticmethod
    async def get_current_user(token: str) -> AppUser:
        try:
            payload = jwt.decode(
                token, app_settings.SECRET_KEY, algorithms=[app_settings.ALGORITHM]
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong token")
        user = await database_worker.custom_orm_select(
            cls_from=AppUser,
            where_params=[AppUser.email == payload.get("sub")],
            return_unpacked=True,
        )
        if not isinstance(user, AppUser):
            raise HTTPException(status_code=401, detail="User not found")
        return user

    @staticmethod
    async def login(
        form_data: OAuth2PasswordRequestForm | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        login_email = form_data.username if form_data else email
        login_password = form_data.password if form_data else password
        if not login_email or not login_password:
            raise HTTPException(status_code=400, detail="Login credentials are missing")

        user = await AuthNamespace._authenticate_user(login_email, login_password)
        access_token_expires = timedelta(
            minutes=int(app_settings.TOKEN_EXPIRES_MINUTES)
        )
        access_token = AuthNamespace._create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def verify_route_access(request: Request, token: str) -> AppUser:
        user = await AuthNamespace.get_current_user(token=token)
        return user
