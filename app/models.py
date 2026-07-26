import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.schemas import IssuePriority, IssueStatus


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    priority: Mapped[str] = mapped_column(String(20), default=IssuePriority.medium.value)
    status: Mapped[str] = mapped_column(String(20), default=IssueStatus.open.value)
