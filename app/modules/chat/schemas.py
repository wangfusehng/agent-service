from uuid import UUID

from pydantic import Field

from app.common.schemas import BaseSchema

# 对话请求类
class ChatRequest(BaseSchema):
    thread_id:UUID
    message:str = Field(min_length=1)



