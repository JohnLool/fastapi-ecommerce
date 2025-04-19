from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_db, delete_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await delete_db()
    yield
    await create_db()


app = FastAPI(lifespan=lifespan)