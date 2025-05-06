from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# define the database models

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    notes = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship with tasks
    tasks = relationship(
        'Task',
        back_populates='project',
        cascade='all, delete-orphan'
    )

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    notes = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)

    # relationship with project
    project = relationship('Project', back_populates='tasks')
