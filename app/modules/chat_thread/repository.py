from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules import chat_thread
from app.modules.chat_thread.models import ChatThread


class ChatThreadRepository:
    """会话管理数据访问层，负责对会话进行增删改查"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, chat_thread: ChatThread):
        self.session.add(chat_thread)

    async def delete(self, chat_thread: ChatThread):
        await self.session.delete(chat_thread)



    async def list_by_user(self,user_id:int)->list[ChatThread]:
        threads = await self.session.scalars(
            select(ChatThread).where(ChatThread.user_id == user_id)
            .order_by(ChatThread.updated_at.desc(),ChatThread.created_at.desc())
        )
        return threads.all()

    async def required_owner(self,user_id:int,id:str)->ChatThread:
        """校验会话是否属于当前用户"""
        chat_thread = await self.session.scalar(
            select(ChatThread)
            .where(ChatThread.id == id,ChatThread.user_id == user_id)
        )
        return chat_thread