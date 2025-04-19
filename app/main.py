from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_db, delete_db
from app.api.users import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await delete_db()
    yield
    await create_db()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)