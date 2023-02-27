from pydantic import BaseModel, Field
from pathlib import Path


class Task(BaseModel):
    name: str
    path: Path
    test_cmd: str = Field(alias="test-cmd")
    short_description: str = Field(alias="short-description")
    long_description: str = Field(alias="long-description")


class EarnFile(BaseModel):
    version: str
    tasks: list[Task]
