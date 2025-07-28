from pymongo import MongoClient
from .config import settings

mongo_client = MongoClient(settings.MONGO_URI)
db = mongo_client[settings.MONGO_DB]

async def close_mongo_connection():
    global mongo_client
    mongo_client.close()
