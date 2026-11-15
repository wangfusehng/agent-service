# 请求和响应约束模型类：用于定义 FastAPI 接口输入输出的字段结构与校验规则。
from decimal import Decimal

from pydantic import field_validator

from app.common.schemas import BaseSchema


class ProductResponse(BaseSchema):
    """保险产品响应模型。负责把数据库对象或接口数据转换成稳定的返回结构。"""

    id: int
    name: str
    clause_name: str
    category: str
    insurer: str
    image_url: str
    description: str
    min_premium: Decimal | None
    max_premium: Decimal | None
    target_group: str | None
    highlights: list[str]
    status: str

    # 规范化高亮点字段：如果前端或数据库传入空值，则统一转换成空列表。
    @field_validator("highlights", mode="before")
    @classmethod
    def normalize_highlights(cls, value: list[str] | None) -> list[str]:
        return value or []