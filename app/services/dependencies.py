from app.services.mongo_db import MongoDB
from typing import Annotated
from fastapi import Depends


async def get_mongo_db() -> MongoDB:
    mongo_db = MongoDB()
    return mongo_db


MongoClient = Annotated[MongoDB, Depends(get_mongo_db)]

