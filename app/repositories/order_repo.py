# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.repositories.base_repo import BaseRepository
# # from app.models.order import OrderOrm
#
# from app.utils.logger import logger
#
#
# class OrderRepository(BaseRepository[OrderOrm]):
#     def __init__(self, session: AsyncSession):
#         super().__init__(OrderOrm, session)