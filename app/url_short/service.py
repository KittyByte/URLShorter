import random
import string

from sqlalchemy import exc

from app.url_short.dao import ShortURLDAO
from app.url_short.schemas import URLShortRedis
from app.services.redis_service import URLRedisService



async def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def create_short_url(original_url: str, owner_id: int | None = None) -> str:
    short_code = await generate_short_code()
    try:
        await ShortURLDAO().create(
            original_url=original_url, short_code=short_code, owner_id=owner_id
        )
    except exc.IntegrityError:
        return await create_short_url(original_url, owner_id)

    return short_code


async def get_url_data_by_code(short_code: str) -> URLShortRedis | None:
    redis_service = URLRedisService()

    if await redis_service.redis.exists(short_code):
        return await redis_service.get_data_by_short_code(short_code)
    else:
        short_url_data = await ShortURLDAO().find_one_by(short_code=short_code)

        if short_url_data:
            await redis_service.set_url_data(short_code, short_url_data)

    return URLShortRedis(**short_url_data) if short_url_data else None

