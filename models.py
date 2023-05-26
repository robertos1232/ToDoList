from enum import Enum
from typing import List
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    mapped_column,
    Mapped
)


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
    name = mapped_column(String(50), nullable=False)
    items: Mapped[List["TodoItem"]] = relationship(
        back_populates='todolist'
    )


class TodoItem(Base):
    __tablename__ = 'todoitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    description = mapped_column(String(50), nullable=False)
    priority = mapped_column(Integer, default=Priority.NON.value)

    todolist_id = mapped_column(String(50), ForeignKey('todolist.id'))
    todolist: Mapped['TodoList'] = relationship(
        back_populates='items'
    )
