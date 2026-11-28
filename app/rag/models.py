from uuid import UUID

from sqlalchemy import BigInteger, String, ARRAY, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.dialects.postgresql import  UUID as PG_UUID
from app.common.models import CreateAtMixin, Base


class ParentChunk(Base,CreateAtMixin):
    """父知识块"""
    __tablename__ = 'parent_chunks'
    id:Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
    )
    product_id:Mapped[int] = mapped_column(BigInteger)
    #条款名称
    clause_name:Mapped[str] = mapped_column(String(300))
    #章节路径
    section_path:Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )
    content:Mapped[str] = mapped_column(Text)
