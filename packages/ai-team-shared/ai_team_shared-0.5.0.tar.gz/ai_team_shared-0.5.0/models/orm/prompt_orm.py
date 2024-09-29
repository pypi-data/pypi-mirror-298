from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm
from ..enums import ModelNameLLM


class UserPromptOrm(BaseOrm):
    __tablename__ = "user_prompts"

    prompt_text: Mapped[str]
    response_class_name: Mapped[Optional[str]]
    input_files: Mapped[list[str]] = mapped_column(JSON)
    output_files: Mapped[list[str]] = mapped_column(JSON)
    llm_model_name: Mapped[ModelNameLLM]
    scoped_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scoped_tasks.id"))
