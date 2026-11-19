from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header,Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database import get_session
from app.modules.chat_thread.schemas import ChatThreadCreate, ChatThreadResponse
from app.modules.chat_thread.service import ChatThreadService

# 路由前缀统一放在 /api/v1/chat-threads 下，便于按模块管理接口。
router = APIRouter(prefix="/api/v1/chat-threads", tags=["会话管理的相关接口"])


# 依赖注入：创建当前请求的 ChatThreadService，并将数据库 session 注入其中。
def get_chat_thread_service(session: AsyncSession = Depends(get_session)):
    # 每次请求都新建一个 service，避免复用状态导致线程安全问题。
    service = ChatThreadService(session)
    yield service


# 新建聊天会话：读取请求体中的标题，并从 Header 中拿到当前登录用户的 ID。
@router.post("", response_model=ChatThreadResponse)
async def create_chat_thread(
    request: ChatThreadCreate,
    service: ChatThreadService = Depends(get_chat_thread_service),
    user_id: Annotated[int, Header(alias="x-user-id")] = ...,
):
    # request.title 已经经过 Pydantic 校验，确保标题不为空且长度合法。
    chat_thread = await service.add(user_id=user_id, title=request.title)
    return chat_thread

@router.get("", response_model=list[ChatThreadResponse])
async def list_by_user(user_id: Annotated[int, Header(alias="x-user-id")] = ...,
                       service: ChatThreadService = Depends(get_chat_thread_service)):
    """查询会话列表"""
    return await service.list_by_user(user_id=user_id)

@router.patch("/{thread_id}", response_model=ChatThreadResponse)
async def rename(
    thread_id: UUID,
    request: ChatThreadCreate,
    user_id: Annotated[int, Header(alias="x-user-id")] = ...,
    service: ChatThreadService = Depends(get_chat_thread_service),
):
    return await service.rename(user_id=user_id, id=str(thread_id), title=request.title)


@router.delete(
    "/{thread_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat_thread(
    thread_id: UUID,
    user_id: Annotated[int, Header(alias="x-user-id")],
    service: ChatThreadService = Depends(get_chat_thread_service),
) -> Response:
    """删除指定会话"""

    await service.delete(thread_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)