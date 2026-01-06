import jwt
from datetime import datetime, timedelta, timezone

from app.settings import settings, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.users.schemas import UserInDB
from app.users.dao import UserDAO



async def verify_password(password: str, hashed_password: str) -> bool:
    return await UserDAO.is_valid_password(password, hashed_password)


async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = await get_user(username)
    if user and await verify_password(password, user.hashed_password):
        return user


async def create_access_token(
    sub: str | int,  # индентификатор пользователя
    data: dict | None = None,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = {
        'sub': sub,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    if data:
        to_encode.update(data)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


async def get_user(username: str) -> UserInDB | None:
    return await UserDAO.find_one_by(username=username)

