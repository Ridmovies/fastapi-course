import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_hotels(client: AsyncClient):
    response = await client.get("/hotels")
    assert response.status_code == 200
    assert len(response.json()) == 6
