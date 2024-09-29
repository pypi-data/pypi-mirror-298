from typing import Optional

from .base_models import BaseApiModel
from .context_models import TaskContext
from .message_models import TaskMessage
from ..enums import ModelNameLLM, AiTaskStatus


class AiTask(BaseApiModel):
    llm_model_name: ModelNameLLM
    prompt_text: str
    status: AiTaskStatus
    user_prompt_id: int
    scoped_task_id: Optional[int] = None
    context: Optional[TaskContext] = None
    messages: list[TaskMessage] = []


class AiCompletion(BaseApiModel):
    success: bool
    text_output: Optional[str] = None
    json_output: Optional[dict] = None
    user_prompt_id: Optional[int] = None
