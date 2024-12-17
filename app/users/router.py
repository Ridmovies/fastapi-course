from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectUserDataException
from app.users.dependencies import get_current_user_id
from app.users.models import User
from app.database import SessionDep
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.schemas import UserAuthSchema, UserOutSchema
from app.users.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_user(
    response: Response, session: SessionDep, user_data: UserAuthSchema
):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectUserDataException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True)
    print(response.__dict__)
    return Response(status_code=204)


@router.post("/register")
async def register(session: SessionDep, user_data: UserAuthSchema):
    exist_user = await UserService.get_one_or_none(email=user_data.email)
    if exist_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.create(email=user_data.email, hashed_password=hashed_password)


@router.get("/me", response_model=UserOutSchema)
async def get_me(
    session: SessionDep, current_user_id: int = Depends(get_current_user_id)
) -> User:
    current_user = await UserService.get_one_or_none(id=current_user_id)
    return current_user
