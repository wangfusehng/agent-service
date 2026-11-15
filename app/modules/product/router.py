#Router只负责HTTP层:声明路径、接收并校验查询参数、注入数据库会，然后把请求交给Service
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database import get_session
from app.modules.product.schemas import ProductResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products",tags=["产品管理的相关接口"])
#依赖注入创建service对象
def get_product_service(session:AsyncSession=Depends(get_session)):
    # 创建service对象
    service = ProductService(session)
    yield service

@router.get("",response_model=list[ProductResponse])
async def list_products(category:str|None=None,
                        service:ProductService=Depends(get_product_service))->list[ProductResponse]:

    # 执行查询
    products = await service.list_products(category)#fastapi会自动把Product类型返回值转换为ProductResponse类型
    return products

@router.get("/candidates", response_model=list[ProductResponse])
async def list_candidates(
    categories: list[str] = Query(min_length=1),
    premium_min: Decimal | None = None,
    limit_per_category: int = 5,
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return await service.list_candidates(
        categories=categories,
        premium_min=premium_min,
        limit_per_category=limit_per_category,
    )