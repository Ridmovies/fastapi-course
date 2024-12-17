import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_booking(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/booking")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_post_booking(authenticated_client: AsyncClient):
    response = await authenticated_client.post("/booking", params={
        "room_id": 1,
        "date_from": "2021-01-01",
        "date_to": "2021-01-02",
    })
    assert response.status_code == 200
    assert response.json()["room_id"] == 1
    assert response.json()["id"] == 4