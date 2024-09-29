from pydantic import BaseModel

from .project_models import (
    KeyResult,
    Objective,
    Requirement,
    ScopedTask,
    ScopedTaskStep,
)


# For specifying and validating the AI completion for project data types


class OKR(BaseModel):
    objective: Objective
    key_results: list[KeyResult]


class KeyResultRequirements(BaseModel):
    key_result: KeyResult
    requirements: list[Requirement]


class ScopedTaskStepList(BaseModel):
    task_id: int
    steps: list[ScopedTaskStep]


class RequirementTasks(BaseModel):
    requirement_id: int
    tasks: list[ScopedTask]
