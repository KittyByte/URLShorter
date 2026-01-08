from pymongo import AsyncMongoClient

from app.settings import db_settings

# TODO добавить сделать пулл подключений

async def get_mongo_client():
    return AsyncMongoClient(db_settings.MONGO_URL)


class BaseMongoDB:
    database = None
    collection = None

    def __init__(self, client: AsyncMongoClient):
        self.client = client

    def get_database(self):
        return self.client.get_database('url_shortener')

    def get_collection(self):
        db = self.get_database()
        return db.get_collection('shortened_urls')

    async def insert_one(self, document: dict) -> None:
        collection = self.get_collection()
        await collection.insert_one(document)

