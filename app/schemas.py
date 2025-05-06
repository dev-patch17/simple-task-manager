from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# task schemas
# the TaskBase model includes fields that are set by the user
class TaskBase(BaseModel):
    name: str
    notes: Optional[str] = None
    completed: bool = False
    project_id: Optional[int] = None

# if we later decide new tasks require additional fields during creation,
# please add them here
class TaskCreate(TaskBase):
    pass

# represents the complete task as it exists in the database
# including fields that cannot be set by the user directly
class Task(TaskBase):
    id: int
    created_at: datetime

    # allow Pydantic to convert ORM objects to dictionaries
    # and access nested relationships
    class Config:
        orm_mode = True


# project schemas follow the same organization as task schemas above
class ProjectBase(BaseModel):
    title: str
    notes: Optional[str] = None
    completed: bool = False

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    tasks: List[Task] = []

    class Config:
        orm_mode = True
