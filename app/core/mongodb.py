import motor.motor_asyncio
from beanie import init_beanie
from app.models.product import Product
from app.core.config import settings


async def init_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client[settings.MONGO_DB_NAME], document_models=[Product])
