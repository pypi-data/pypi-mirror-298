from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm
from ..enums import MessageRole


class TaskMessageOrm(BaseOrm):
    __tablename__ = "task_messages"

    content: Mapped[str]
    role: Mapped[MessageRole]
    ai_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ai_tasks.id"))
