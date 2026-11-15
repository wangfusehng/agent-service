from uuid import UUID, uuid4

from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base, CreateAtMixin, UpdateAtMixin


class ChatThread(Base, CreateAtMixin, UpdateAtMixin):
    """客服会话表，记录一次用户和客服/助手之间的对话线程。"""

    __tablename__ = "chat_threads"

    # 线程唯一标识，使用 PostgreSQL 的 UUID 类型，便于跨系统追踪会话。
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # 关联的用户 ID，使用 BigInteger 以兼容大多数数据库中的长整型用户标识。
    user_id: Mapped[int] = mapped_column(BigInteger)

    # 会话标题，默认是“新会话”，并同步写入数据库默认值，避免空值。
    title: Mapped[str] = mapped_column(
        String(200),
        default="新会话",
        server_default="新会话",
    )