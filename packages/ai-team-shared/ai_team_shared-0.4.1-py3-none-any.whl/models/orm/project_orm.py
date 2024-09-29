from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_orm import BaseOrm
from ..enums import StatusType, AssigneeType, NecessityType, PriorityType, TaskType


class BaseProjectOrm(BaseOrm):
    __abstract__ = True

    description: Mapped[str]
    status: Mapped[StatusType] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(index=True)


class ProjectOrm(BaseProjectOrm):
    __tablename__ = "projects"


class ObjectiveOrm(BaseProjectOrm):
    __tablename__ = "objectives"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    # project: Mapped["Project"] = relationship(back_populates="objectives")
    # key_results: Mapped[list["KeyResult"]] = relationship(back_populates="objective")


class KeyResultOrm(BaseProjectOrm):
    __tablename__ = "key_results"

    objective_id: Mapped[int] = mapped_column(ForeignKey("objectives.id"))
    # objective: Mapped["Objective"] = relationship(back_populates="key_results")
    # requirements: Mapped[list["Requirement"]] = relationship(back_populates="key_result")


class RequirementOrm(BaseProjectOrm):
    __tablename__ = "requirements"

    necessity: Mapped[NecessityType]
    key_result_id: Mapped[int] = mapped_column(ForeignKey("key_results.id"))
    # key_result: Mapped["KeyResult"] = relationship(back_populates="requirements")
    # scoped_tasks: Mapped[list["ScopedTask"]] = relationship(back_populates="requirement")


class ScopedTaskOrm(BaseProjectOrm):
    __tablename__ = "scoped_tasks"

    assignee: Mapped[Optional[AssigneeType]]
    priority: Mapped[Optional[PriorityType]]
    task_type: Mapped[TaskType] = mapped_column(default=TaskType.UNDEFINED)
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirements.id"))
    # requirement: Mapped["Requirement"] = relationship(back_populates="scoped_tasks")
    # steps: Mapped[list["ScopedTaskStep"]] = relationship(back_populates="task")


class ScopedTaskStepOrm(BaseOrm):
    __tablename__ = "scoped_task_steps"

    action: Mapped[str]
    status: Mapped[StatusType]
    expected_result: Mapped[Optional[str]]
    task_id: Mapped[int] = mapped_column(ForeignKey("scoped_tasks.id"))
    # task: Mapped["ScopedTask"] = relationship(back_populates="steps")
