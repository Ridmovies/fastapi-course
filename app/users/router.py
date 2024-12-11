from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select

from app.users.models import User
from app.database import SessionDep
from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from app.users.schemas import UserAuthSchema
from app.users.services import UserService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
async def login_user(response: Response, session: SessionDep, user_data: UserAuthSchema):
    user = await authenticate_user(session, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')
    access_token = create_access_token({'sub': user.id})
    response.set_cookie('access_token', access_token, httponly=True)
    return access_token


@router.post('/register')
async def register(session: SessionDep, user_data: UserAuthSchema):
    exist_user = await UserService.get_one_or_none(session, email=user_data.email)
    if exist_user:
        raise HTTPException(status_code=400, detail='User already exist')
    hashed_password = get_password_hash(user_data.password)
    await UserService.create(session, email=user_data.email, hashed_password=hashed_password)