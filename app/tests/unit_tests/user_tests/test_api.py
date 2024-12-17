import logging
import pytest
from httpx import AsyncClient
from app.users.services import UserService


@pytest.mark.anyio
async def test_root(caplog, client: AsyncClient):
    # caplog.set_level(logging.INFO)
    response = await client.get("/")
    assert response.status_code == 200
    # logging.info(f"Response content: {response}")


@pytest.mark.asyncio
@pytest.mark.parametrize("email,password,status_code", [
                         ('example@example.com', 'example', 200),
                         ('example@example.com', 'example', 409),
                ('example', 'example', 422),
                ('1234455@example.com', '1234455', 200),

])
async def test_register_user(
        email: str,
        password: str,
        status_code: int,
        client: AsyncClient
) -> None:
    response = await client.post("/users/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code



@pytest.mark.asyncio
@pytest.mark.parametrize("email,password,status_code", [
                         ('test@test.com', 'test', 409),
                         ('artem@example.com', 'artem', 409),
                ('example', 'example', 422),
                ('1234455@example.com', '1234455', 409),

])
async def test_login_user(
        email: str,
        password: str,
        status_code: int,
        client: AsyncClient
) -> None:
    response = await client.post("/users/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, email, is_present",[
    (1, "test@test.com", True),
    (2, 'artem@example.com', True),
    (3, "example@example.com", True),
    (999, "example@example.com", False),
])
async def test_find_user_by_id(user_id, email, is_present):
    user = await UserService.get_one_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
