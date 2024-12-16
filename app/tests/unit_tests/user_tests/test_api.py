import pytest
from httpx import AsyncClient


# async def test_register_user(async_client: AsyncClient):
#     response = await async_client.post("/users/auth/register", json={
#         "email": "example@example.com",
#         "password": "test"
#     })
#     assert response.status_code == 200


class TestUsers:
    @pytest.mark.asyncio
    async def test_me(self, async_client: AsyncClient):
        response = await async_client.get("/users/auth/me")
        assert response.status_code == 200