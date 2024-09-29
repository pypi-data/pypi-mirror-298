from pydantic import Field

from .base_models import BaseApiModel
from ..enums import UserRole


class User(BaseApiModel):
    name: str = Field(..., description="User's name")
    role: UserRole = Field(..., description="User's role")
