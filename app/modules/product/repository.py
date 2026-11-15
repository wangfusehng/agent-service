from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Product
class ProductRepository:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def query_by_category(self, category: str | None=None)->list[Product]:
        #动态条件，产品必须是上架的产品
        conditions= [Product.status == 'active']
        #如果category不为空，追加相应的查询条件
        if category:
            conditions.append(Product.category == category)

        # result = await self.session.execute(
        #     select(Product).where(*conditions).order_by(Product.id.asc())
        # )
        #
        # return result.scalars().all()

        result = await self.session.scalars(select(Product).where(*conditions))
        return result.all()