from redis.asyncio import Redis, ConnectionPool
from app.settings import db_settings


redis_pool = ConnectionPool.from_url(db_settings.REDIS_URL)


class RedisService:
    def __init__(self):
        self.redis = Redis(connection_pool=redis_pool)



