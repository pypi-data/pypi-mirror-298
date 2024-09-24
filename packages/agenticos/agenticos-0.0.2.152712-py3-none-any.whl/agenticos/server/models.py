from enum import Enum
from uuid import UUID, uuid4
from typing import Callable

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Workflow(BaseModel):
    name: str
    description: str
    inputs: dict[str, str]
    kickoff_function: Callable[[dict[str, str]], None] = Field(exclude=True)
    output_function: Callable[[], str] = Field(exclude=True)


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    inputs: dict[str, str]
    status: TaskStatus
    output: str
