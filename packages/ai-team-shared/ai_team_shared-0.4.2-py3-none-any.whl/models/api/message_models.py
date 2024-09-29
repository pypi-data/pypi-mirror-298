from typing import Optional

from .base_models import BaseApiModel
from ..enums import MessageRole


# TODO: consider merging this module into ai_task_models.py


class TaskMessage(BaseApiModel):
    content: str
    role: MessageRole
    ai_task_id: Optional[int] = None
