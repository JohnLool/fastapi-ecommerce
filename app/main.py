from contextlib import asynccontextmanager

from fastapi import FastAPI

# from app.core.database import create_db, delete_db
from app.api.users import router as users_router
from app.core.mongodb import init_mongo


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await delete_db()
    await init_mongo()
    yield
    # await create_db()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
