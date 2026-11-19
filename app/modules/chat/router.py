from typing import Annotated

from fastapi import APIRouter, Depends, Header,Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.chat.schemas import ChatRequest
from app.modules.chat.service import ChatService

router = APIRouter(prefix="/api/v1/chat",tags=["agent对话相关的接口"])
def get_chat_service(http_request:Request,session:AsyncSession = Depends(get_session)):
    agent = http_request.app.state.agent
    return ChatService(session, agent)
@router.post("")
async def chat(request:ChatRequest,
               user_id: Annotated[int, Header(alias="x-user-id")] = ...,
               service:ChatService = Depends(get_chat_service),):
    response = await service.chat_stream(user_id,request)
    return response
