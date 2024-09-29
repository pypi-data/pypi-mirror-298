from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_orm import BaseOrm
from .context_orm import TaskContextOrm
from .message_orm import TaskMessageOrm
from ..enums import ModelNameLLM, AiTaskStatus


class AiTaskOrm(BaseOrm):
    __tablename__ = "ai_tasks"

    llm_model_name: Mapped[ModelNameLLM]
    prompt_text: Mapped[str]
    status: Mapped[AiTaskStatus]
    user_prompt_id: Mapped[int] = mapped_column(ForeignKey("user_prompts.id"))
    scoped_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scoped_tasks.id"))
    context: Mapped[Optional[TaskContextOrm]] = relationship(lazy="selectin")
    messages: Mapped[list[TaskMessageOrm]] = relationship(lazy="selectin")
