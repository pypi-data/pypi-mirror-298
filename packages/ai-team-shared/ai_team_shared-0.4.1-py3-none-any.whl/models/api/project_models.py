from typing import Optional

from .base_models import BaseApiModel
from ..enums import StatusType, AssigneeType, NecessityType, PriorityType, TaskType


class BaseProjectModel(BaseApiModel):
    description: str
    status: StatusType
    name: str


class Project(BaseProjectModel):
    pass


class Objective(BaseProjectModel):
    project_id: int


class KeyResult(BaseProjectModel):
    objective_id: int


class Requirement(BaseProjectModel):
    key_result_id: int
    necessity: NecessityType


class ScopedTask(BaseProjectModel):
    requirement_id: int
    assignee: Optional[AssigneeType] = None
    priority: Optional[PriorityType] = None
    task_type: TaskType = TaskType.UNDEFINED

    # Additional fields to provide more information
    # estimated_duration: Optional[str]
    # difficulty: Optional[str]

    # This can be used to link the task to Gitlab MR
    # merge_request_id: Optional[str] = None


class ScopedTaskStep(BaseApiModel):
    task_id: int
    action: str
    status: StatusType
    expected_result: Optional[str] = None
    # consider adding execution_log here
