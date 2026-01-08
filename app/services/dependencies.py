from typing import Annotated
from fastapi import Depends

from app.services.mongo_db import get_mongo_client, AsyncMongoClient
from app.services.redis_service import get_redis_client, Redis



MongoClientDep = Annotated[AsyncMongoClient, Depends(get_mongo_client)]
RedisClientDep = Annotated[Redis, Depends(get_redis_client)]

