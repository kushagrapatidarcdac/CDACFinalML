import motor.motor_asyncio
from .config import settings

mongo_client = None
db=None

async def connect_to_mongo():
    global db
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    db = mongo_client[settings.MONGO_DB]

async def close_mongo_connection():
    global mongo_client
    mongo_client.close()

if __name__ == "__main__":
    connect_to_mongo()
    