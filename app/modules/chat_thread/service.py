from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat_thread.models import ChatThread
from app.modules.chat_thread.repository import ChatThreadRepository
from app.modules.chat_thread.schemas import ChatThreadResponse


class ChatThreadService:
    """会话业务层，用于处理创建新聊天会话的业务逻辑。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repositroy = ChatThreadRepository(session)

    async def add(self, user_id: int, title: str):
        """创建新的聊天，并在事务中保存到数据库。"""
        async with self.session.begin():
            # 组装会话实体：用户 ID 与标题是创建的最基本信息。
            chat_thread = ChatThread(user_id=user_id, title=title)
            # 持久化到仓储层，确保数据库写入在事务中完成。
            await self.repositroy.add(chat_thread=chat_thread)
            return chat_thread
    async def list_by_user(self,user_id:int)->list[ChatThreadResponse]:
        return await self.repositroy.list_by_user(user_id=user_id)