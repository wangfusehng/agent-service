from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product
from app.modules.product.repository import ProductRepository


class ProductService:
    """产品业务服务，负责编排查询和筛选逻辑。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepository(session)

    async def list_products(self, category: str | None = None) -> list[Product]:
        """返回指定分类的在售产品，若未传分类则返回全部在售产品。"""
        return await self.repository.query_by_category(category)

    async def list_candidates(
        self,
        categories: list[str],
        premium_min: Decimal | None,
        limit_per_category: int,
    ) -> list[Product]:
        """按分类循环查询候选产品，并去重后汇总结果。"""
        return await self.repository.find_candidates(
            categories=categories,
            premium_min=premium_min,
            limit_per_category=limit_per_category
        )