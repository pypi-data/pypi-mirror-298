from typing import Optional

from pydantic import BaseModel

from .base_models import BaseApiModel
from .project_models import Project, Objective, KeyResult, Requirement, ScopedTask


# TODO: consider merging into ai_task_models.py


class TaskResponseFormat(BaseModel):
    data_model_class: str
    data_model_schema: Optional[dict] = None
    data_model_example: Optional[dict] = None


class ProjectContext(BaseModel):
    project: Project
    objective: Objective
    key_result: KeyResult
    requirement: Requirement
    scoped_task: ScopedTask


class FileContext(BaseModel):
    file_uri: str
    file_content: Optional[str] = None


class TaskContext(BaseApiModel):
    response_format: Optional[TaskResponseFormat] = None
    project_context: Optional[ProjectContext] = None
    input_files: list[FileContext] = []
    output_files: list[str] = []
    ai_task_id: Optional[int] = None
    scoped_task_id: Optional[int] = None
