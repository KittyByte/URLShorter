import bcrypt

from app.orm.dao import BaseDAO
from app.users.models import UserOrm
from app.users.schemas import UserInDB


class UserDAO(BaseDAO):
    model = UserOrm

    @classmethod
    async def _hash_password(cls, password: str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    @classmethod
    async def find_one_by(cls, **filter_by):
        user = await super().find_one_by(**filter_by)
        return UserInDB(**user) if user else None

    @classmethod
    async def create(cls, **data):
        data['password'] = cls._hash_password(data['password'])
        return await super().create(**data)
    
    @classmethod
    async def create_bulk(cls, values):
        for value in values:
            value['password'] = cls._hash_password(value['password'])
        return await super().create_bulk(values)

    @classmethod
    async def is_valid_password(cls, password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
