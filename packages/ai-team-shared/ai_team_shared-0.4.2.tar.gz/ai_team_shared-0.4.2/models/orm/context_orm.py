from typing import Optional

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm


class TaskContextOrm(BaseOrm):
    __tablename__ = "task_contexts"

    response_format: Mapped[Optional[dict]] = mapped_column(JSON)
    project_context: Mapped[Optional[dict]] = mapped_column(JSON)
    input_files: Mapped[list[dict]] = mapped_column(JSON)
    output_files: Mapped[list[str]] = mapped_column(JSON)
    ai_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ai_tasks.id"))
    scoped_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scoped_tasks.id"))
