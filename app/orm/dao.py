from sqlalchemy import delete, insert, select, update

from app.database import session_factory


class BaseDAO:
    model = None

    @classmethod
    async def find_one_by(cls, **filter_by) -> dict:
        async with session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            res = await session.execute(query)
            return res.mappings().one_or_none()

    @classmethod
    async def find_all_by(cls, **filter_by) -> list[dict]:
        async with session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            res = await session.execute(query)
            return res.mappings().all()

    @classmethod
    async def create(cls, **data) -> int:
        async with session_factory() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()['id']

    @classmethod
    async def create_bulk(cls, values: list[dict]) -> list[int]:
        async with session_factory() as session:
            query = insert(cls.model).values(values).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return [_id['id'] for _id in result.mappings().all()]

    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with session_factory() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_where(cls, where_clause) -> dict:
        async with session_factory() as session:
            query = select(cls.model.__table__.columns).filter(where_clause)
            res = await session.execute(query)
            return res.mappings().one_or_none()

    @classmethod
    async def find_all_where(cls, *filters) -> list[dict]:
        """Поиск всех записей по сложным условиям"""
        async with session_factory() as session:
            query = select(cls.model.__table__.columns).filter(*filters)
            res = await session.execute(query)
            return res.mappings().all()

    @classmethod
    async def update(cls, obj_id: int, **update_data) -> None:
        async with session_factory() as session:
            query = update(cls.model).filter_by(id=obj_id).values(update_data)
            await session.execute(query)
            await session.commit()

