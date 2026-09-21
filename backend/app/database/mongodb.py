from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client


def get_db():
    return get_client()[settings.DATABASE_NAME]


def users_collection():
    return get_db()["users"]


def assessments_collection():
    return get_db()["assessments"]


def recommendations_collection():
    return get_db()["recommendations"]


def chatbot_sessions_collection():
    return get_db()["chatbot_sessions"]


async def close_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None
