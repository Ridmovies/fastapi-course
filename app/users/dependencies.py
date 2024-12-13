from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpireException, TokenInvalidException, NotAuthUserException


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise NotAuthUserException
    return access_token


async def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise TokenInvalidException
    user_id: int = int(payload.get('sub'))
    expire = payload.get('exp')
    if expire < datetime.utcnow().timestamp():
        raise TokenExpireException
    print(f"user_id: {user_id}")
    return user_id