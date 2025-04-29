from contextlib import asynccontextmanager

from fastapi import FastAPI

# from app.core.database import create_db, delete_db
from app.api.users import router as users_router
from app.api.categories import router as categories_router
from app.api.products import router as products_router
from app.api.shops import router as shops_router
from app.core.mongodb import init_mongo


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await delete_db()
    await init_mongo()
    yield
    # await create_db()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(shops_router)
