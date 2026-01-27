from redis.asyncio import Redis

from app.settings import redis_pool
from app.url_short.schemas import URLShortRedis



def get_redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)


class BaseRedisService:
    def __init__(self):
        self.redis: Redis = get_redis_client()



EXPIRED_TIME = 86400  # 1 day

class URLRedisService(BaseRedisService):
    async def set_url_data(self, short_code: str, data: dict) -> None:
        data = URLShortRedis(**data).model_dump(exclude_none=True, mode='json')

        await self.redis.hset(short_code, mapping=data)
        await self.redis.expire(short_code, EXPIRED_TIME)

    async def get_data_by_short_code(self, short_code: str) -> URLShortRedis | None:
        data = await self.redis.hgetall(short_code)
        return URLShortRedis(**data) if data else None
