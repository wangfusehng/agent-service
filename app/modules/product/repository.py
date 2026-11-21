from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


class ProductRepository:
    """产品数据访问层，负责查询在售产品及其筛选结果。"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def query_by_category(self, category: str | None = None) -> list[Product]:
        """按分类查询已上架的产品；category 为空时查询全部在售产品。"""
        # 仅返回状态为 active 的产品，确保只查询已上架数据。
        conditions = [Product.status == "active"]

        # 如果提供分类参数，则进一步过滤对应类别的产品。
        if category:
            conditions.append(Product.category == category)

        # result = await self.session.execute(
        #     select(Product).where(*conditions).order_by(Product.id.asc())
        # )
        #
        # return result.scalars().all()

        result = await self.session.scalars(select(Product).where(*conditions))
        return result.all()

    async def find_limited_by_category(
            self,
            category: str,
            premium_min: Decimal | None,
            limit: int,
    ) -> list[Product]:
        conditions = [
            Product.status == "active",
            Product.category == category,
        ]
        if premium_min is not None:
            conditions.append(Product.min_premium < premium_min)

        products = await self.session.scalars(
            select(Product)
            .where(*conditions)
            .order_by(
                Product.min_premium.asc().nullslast(),
                Product.id.asc(),
            )
            .limit(limit)
        )
        return products.all()