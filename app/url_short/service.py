import random
import string

from sqlalchemy import exc

from app.url_short.dao import ShortURLDAO
from app.url_short.schemas import ShortenURL



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


async def get_url_data_by_code(short_code: str) -> ShortenURL | None:
    short_url = await ShortURLDAO().find_one_by(short_code=short_code)
    if short_url:
        return ShortenURL(**short_url)
    return short_url

