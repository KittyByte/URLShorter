from argon2 import PasswordHasher
from asyncio import to_thread

from app.orm.dao import BaseDAO
from app.users.models import UserModel
from app.users.schemas import UserInDB


ph = PasswordHasher()


class UserDAO(BaseDAO):
    model = UserModel

    @classmethod
    async def _hash_password(cls, password: str):
        return await to_thread(ph.hash, password)

    @classmethod
    async def find_one_by(cls, **filter_by):
        user = await super().find_one_by(**filter_by)
        return UserInDB(**user) if user else None

    @classmethod
    async def create(cls, **data):
        data['password'] = await cls._hash_password(data['password'])
        return await super().create(**data)

    @classmethod
    async def create_bulk(cls, values):
        for value in values:
            value['password'] = await cls._hash_password(value['password'])
        return await super().create_bulk(values)

    @classmethod
    async def is_valid_password(cls, password: str, hashed_password: str) -> bool:
        return await to_thread(ph.verify, hashed_password, password)
