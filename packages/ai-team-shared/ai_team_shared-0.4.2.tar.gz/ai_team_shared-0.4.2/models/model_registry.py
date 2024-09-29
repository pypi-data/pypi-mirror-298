from typing import Type

from ai_team_shared.models.api.ai_task_models import AiTask
from ai_team_shared.models.api.base_models import BaseApiModel
from ai_team_shared.models.api.context_models import TaskContext
from ai_team_shared.models.api.message_models import TaskMessage
from ai_team_shared.models.api.project_models import (
    Project,
    Objective,
    KeyResult,
    Requirement,
    ScopedTask,
    ScopedTaskStep,
)
from ai_team_shared.models.api.prompt_models import UserPrompt
from ai_team_shared.models.api.user_models import User
from ai_team_shared.models.orm.ai_task_orm import AiTaskOrm
from ai_team_shared.models.orm.base_orm import BaseOrm
from ai_team_shared.models.orm.context_orm import TaskContextOrm
from ai_team_shared.models.orm.message_orm import TaskMessageOrm
from ai_team_shared.models.orm.project_orm import (
    ProjectOrm,
    ObjectiveOrm,
    KeyResultOrm,
    RequirementOrm,
    ScopedTaskOrm,
    ScopedTaskStepOrm,
)
from ai_team_shared.models.orm.prompt_orm import UserPromptOrm
from ai_team_shared.models.orm.user_orm import UserOrm

# Register all models here
MODEL_REGISTRY: dict[Type[BaseApiModel], Type[BaseOrm]] = {
    User: UserOrm,
    Project: ProjectOrm,
    Objective: ObjectiveOrm,
    KeyResult: KeyResultOrm,
    Requirement: RequirementOrm,
    ScopedTask: ScopedTaskOrm,
    ScopedTaskStep: ScopedTaskStepOrm,
    UserPrompt: UserPromptOrm,
    AiTask: AiTaskOrm,
    TaskContext: TaskContextOrm,
    TaskMessage: TaskMessageOrm,
}
