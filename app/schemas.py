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