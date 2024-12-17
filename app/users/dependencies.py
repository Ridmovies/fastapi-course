from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    NotAuthUserException,
    TokenExpireException,
    TokenInvalidException,
)
from app.users.models import User
from app.users.services import UserService


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise NotAuthUserException
    return access_token


async def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise TokenInvalidException
    user_id: int = int(payload.get("sub"))
    expire = payload.get("exp")
    if expire < datetime.utcnow().timestamp():
        raise TokenExpireException
    return user_id


async def get_current_user(
    access_token: str = Depends(get_access_token),
) -> User | None:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise TokenInvalidException
    user_id: int = int(payload.get("sub"))
    expire = payload.get("exp")
    if expire < datetime.utcnow().timestamp():
        raise TokenExpireException

    user: User | None = await UserService.get_one_by_id(user_id)
    return user
