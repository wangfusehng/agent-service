from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat_thread.exceptions import ChatThreadNotFound
from app.modules.chat_thread.models import ChatThread
from app.modules.chat_thread.repository import ChatThreadRepository
from app.modules.chat_thread.schemas import ChatThreadResponse


class ChatThreadService:
    """会话业务层，用于处理创建新聊天会话的业务逻辑。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ChatThreadRepository(session)

    async def add(self, user_id: int, title: str):
        """创建新的聊天，并在事务中保存到数据库。"""
        async with self.session.begin():
            # 组装会话实体：用户 ID 与标题是创建的最基本信息。
            chat_thread = ChatThread(user_id=user_id, title=title)
            # 持久化到仓储层，确保数据库写入在事务中完成。
            await self.repository.add(chat_thread=chat_thread)
            return chat_thread
    async def list_by_user(self,user_id:int)->list[ChatThreadResponse]:
        return await self.repository.list_by_user(user_id=user_id)

    async def rename(self,user_id:int,id:str,title:str)->ChatThreadResponse:
        async with self.session.begin():#开启事务
            # 1.查询会话，校验会话是否属于当前用户
            chat_thread = await self.repository.required_owner(user_id=user_id,id=id)
            if not chat_thread:
                raise ChatThreadNotFound()

            #2.修改标题
            chat_thread.title = title
            #手动刷新数据
            await self.session.flush()
            await self.session.refresh(chat_thread)
            return chat_thread

    async def delete(
            self,
            chat_thread_id: UUID,
            user_id: int,
    ) -> None:
        async with self.session.begin():
            thread = await self.repository.required_owner(user_id=user_id,id=chat_thread_id, )
            if thread is None:
                raise ChatThreadNotFound

            await self.repository.delete(thread)