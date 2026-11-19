from fastapi.sse import ServerSentEvent
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.schemas import ChatRequest
from app.modules.chat_thread.exceptions import ChatThreadNotFound
from app.modules.chat_thread.repository import ChatThreadRepository


# langchain帮忙完成了对话的持久化和管理，不需要自定义model类和repository类

class ChatService:
    def __init__(self,session:AsyncSession,agent:CompiledStateGraph):
        self.agent = agent
        self.repository = ChatThreadRepository(session)

    async def chat_stream(self,user_id:int,request:ChatRequest,):
        """实现agent流式对话的函数"""
        #判断当前的会话是否属于请求的用户
        chat_thread = await self.repository.required_owner(user_id,request.thread_id)
        if not chat_thread:
            #会话不属于当前用户
            raise ChatThreadNotFound()
        # 将用户消息封装为 LangGraph 可识别的输入格式
        user_input = {"messages":[HumanMessage(request.message)]}
        # thread_id 用于标识会话，使 LangGraph 复用对应的对话历史
        config = {"configurable":{"thread_id":request.thread_id}}
        # 异步调用 agent，
        stream_response = await self.agent.astream_events(
            input = user_input,
            config = config,
            version="v3"
        )
        async for message in stream_response.messages:
            async for chunk in message.text:
                yield ServerSentEvent(data=chunk,event="message")
        yield ServerSentEvent(data="END",event="done")
