import motor.motor_asyncio
from beanie import init_beanie
from app.models.product import Product
from app.core.config import settings


async def init_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    await init_beanie(database=db, document_models=[Product])
