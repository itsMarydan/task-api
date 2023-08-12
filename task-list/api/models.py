from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from db import Base

class TaskEntity(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    #id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    created_by = Column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="tasks")

class UserEntity(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    #id = Column(Integer, primary_key=True, index=True)
    fname = Column(String,index=True)
    lname = Column(String,index=True)

    tasks: Mapped[List["TaskEntity"]] = relationship(back_populates="user")