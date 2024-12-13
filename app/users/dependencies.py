from datetime import datetime

from fastapi import Request, HTTPException, Depends
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import SessionDep
from app.users.models import User
from app.users.services import UserService


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided")
    return access_token


async def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id: int = int(payload.get('sub'))
    expire = payload.get('exp')
    if expire < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Access token expired")
    print(f"user_id: {user_id}")
    return user_id