import asyncio
import json
from asyncio import BaseEventLoop
from datetime import datetime
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session, async_engine, Base
from app.hotels.models import Hotel
from app.users.models import User
from app.rooms.models import Room
from app.booking.models import Booking
from main import app as test_app

@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    if settings.MODE != 'TEST':
        raise Exception

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def _open_mock_json(model: str) -> dict:
        mock_file = f'app/tests/mock_{model}.json'
        with open(mock_file, 'r', encoding='utf-8') as open_file:
            return json.load(open_file)


    hotels = _open_mock_json(model='hotels')
    # rooms = _open_mock_json(model='rooms')
    users = _open_mock_json(model='users')
    # bookings_ = _open_mock_json(model='bookings')

    # for d in bookings_:
    #     d['date_from'] = datetime.strptime(d['date_from'], '%Y-%m-%d')
    #     d['date_to'] = datetime.strptime(d['date_to'], '%Y-%m-%d')
    #
    async with async_session() as session:
        add_hotels = insert(Hotel).values(hotels)
    #     add_rooms = insert(Room).values(rooms)
        add_users = insert(User).values(users)
    #     add_bookings = insert(Booking).values(bookings_)
    #
        await session.execute(add_hotels)
    #     await session.execute(add_rooms)
        await session.execute(add_users)
    #     await session.execute(add_bookings)

        await session.commit()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test",
    ) as ac:
        yield ac


# @pytest.fixture()
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
#
#
# @pytest.fixture
# def test_app(db_session: AsyncSession) -> FastAPI:
#     """Create a test app with overridden dependencies."""
#     fastapi_app.dependency_overrides[get_session] = lambda: prepare_database
#     return fastapi_app
#
#
# @pytest_asyncio.fixture
# async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
#     """Create a http client."""
#     async with AsyncClient(
#         transport=ASGITransport(app=test_app),
#         base_url="http://test",
#     ) as a_client:
#         yield a_client