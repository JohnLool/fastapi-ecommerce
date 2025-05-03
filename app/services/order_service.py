# from typing import Optional
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.repositories.order_repo import OrderRepository
#
# from app.schemas.order import OrderOut, OrderCreate, OrderUpdate
#
# from app.services.base_service import BaseService
# from app.utils.logger import logger
#
#
# class OrderService(BaseService[OrderRepository]):
#     def __init__(self, db: AsyncSession):
#         super().__init__(OrderRepository(db), OrderOut)