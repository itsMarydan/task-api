from sqlalchemy import Column, String, Boolean, TIMESTAMP, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from typing import List


Base = declarative_base()

class TaskEntity(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("UserEntity", back_populates="tasks")

class UserEntity(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    fname = Column(String,index=True)
    lname = Column(String,index=True)

    tasks = relationship("TaskEntity", back_populates="user")