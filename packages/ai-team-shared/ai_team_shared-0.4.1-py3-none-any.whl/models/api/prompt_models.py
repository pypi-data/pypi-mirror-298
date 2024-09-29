from typing import Optional

from .base_models import BaseApiModel
from ..enums import ModelNameLLM


class UserPrompt(BaseApiModel):
    prompt_text: str
    response_class_name: Optional[str] = None
    input_files: list[str] = []
    output_files: list[str] = []
    llm_model_name: ModelNameLLM
    scoped_task_id: Optional[int] = None

    # consider adding
    # - additional LLM model config fields (e.g., temperature)
    # - user_id field
