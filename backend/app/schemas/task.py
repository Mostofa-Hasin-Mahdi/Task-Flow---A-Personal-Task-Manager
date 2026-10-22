from datetime import datetime
from typing import Any, Generic, List, Literal, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

T = TypeVar("T")


class TaskCreate(BaseModel):
    """Schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise ValueError("Title must be a string")
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or only whitespace")
        if len(stripped) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        return stripped

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            stripped = v.strip()
            return stripped if stripped else None
        return v


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["pending", "completed"]] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not isinstance(v, str):
            raise ValueError("Title must be a string")
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or only whitespace")
        if len(stripped) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        return stripped

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            stripped = v.strip()
            return stripped if stripped else None
        return v

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "TaskUpdate":
        if self.title is None and self.description is None and self.status is None:
            raise ValueError("At least one field must be provided for update")
        return self


class TaskRead(BaseModel):
    """Schema for reading task details."""

    id: int
    title: str
    description: Optional[str] = None
    status: Literal["pending", "completed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DataEnvelope(BaseModel, Generic[T]):
    """Consistent JSON response envelope: {"data": ...}"""

    data: T


class TaskResponse(DataEnvelope[TaskRead]):
    pass


class TaskListResponse(DataEnvelope[List[TaskRead]]):
    pass


class TaskDeleteResponse(DataEnvelope[dict]):
    pass
