from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

# 定义一个通用泛型
T = TypeVar('T')
#定义一个基础响应模型，便于之后的子类响应模型继承，来自动执行数据模型->响应模型的转化
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PageResult(BaseSchema,Generic[T]):
    """通用分页结果"""
    items:list[T]
    page: int
    page_size: int
    total: int