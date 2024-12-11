from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_id(cls, session: AsyncSession, model_id:int):
        query = select(cls.model).filter_by(id=int(model_id))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, session: AsyncSession, **data):
        instance = cls.model(**data)
        session.add(instance)
        await session.commit()
        return instance