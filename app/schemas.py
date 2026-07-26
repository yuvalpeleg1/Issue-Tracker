from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class IssueStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: IssuePriority = IssuePriority.medium


class IssueUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=5, max_length=1000)
    priority: IssuePriority | None = None
    status: IssueStatus | None = None


class IssueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssueStatus
