from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Column
from sqlalchemy.sql import func
from api.db import Base


class TaskEntity(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    created_by = Column(String)
