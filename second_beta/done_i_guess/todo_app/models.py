from enum import Enum
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    mapped_column,
    Mapped
)
from pydantic import BaseModel


class Priority(Enum):
    NON = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Base(DeclarativeBase):
    pass


class TodoList(Base):
    __tablename__ = 'todolist'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    items: Mapped[List["TodoItem"]] = relationship(
        back_populates='todolist'
    )


class TodoItem(Base):
    __tablename__ = 'todoitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    description = mapped_column(String(50), nullable=False)
    priority = mapped_column(Integer, default=Priority.NON.value)
    done = mapped_column(Boolean, default=False)

    todolist_id = mapped_column(String(50), ForeignKey('todolist.id'))
    todolist: Mapped['TodoList'] = relationship(
        back_populates='items'
    )


class TodoListSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class TodoItemSchema(BaseModel):
    description: str = ""
    priority: int = 0
    done: bool = False

    class Config:
        orm_mode = True
