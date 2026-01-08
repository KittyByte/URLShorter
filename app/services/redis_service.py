from redis.asyncio import Redis, ConnectionPool

from app.settings import db_settings
from app.url_short.schemas import URLShortRedis



redis_pool = ConnectionPool.from_url(db_settings.REDIS_URL, decode_responses=True)


def get_redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)


class BaseRedisService:
    def __init__(self):
        self.redis: Redis = get_redis_client()



class URLRedisService(BaseRedisService):
    async def set_url_data(self, short_code: str, data: dict) -> None:
        data = URLShortRedis(**data).model_dump(exclude_none=True)

        await self.redis.hset(short_code, mapping=data)
        await self.redis.expire(short_code, 86400)  # 1 day

    async def get_data_by_short_code(self, short_code: str) -> URLShortRedis | None:
        data = await self.redis.hgetall(short_code)
        return URLShortRedis(**data) if data else None
