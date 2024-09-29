from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseApiModel(BaseModel):
    """
    Base class for all API models
    - Subclass of Pydantic BaseModel
    - Used for data validation and serialization in API layer
    """

    id: Optional[int] = Field(default=None, description="Unique identifier for the model")
    created_at: datetime = Field(default_factory=utc_now, description="Timestamp of when the record was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp of when the record was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        # enable validate_assignment if we want to validate whenever updating model attributes
        # validate_assignment=True,
    )
