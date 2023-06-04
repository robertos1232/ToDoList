from abc import ABC, abstractmethod
from typing import Type

from todo_app.models import TodoList, TodoItem

from sqlalchemy import Engine
from sqlalchemy.orm import Session


class CRUDCommand(ABC):
    def __init__(self, item: TodoList | TodoItem, engine: Engine):
        self.item = item
        self.engine = engine

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class CreateItem(CRUDCommand):
    def execute(self, *args, **kwargs):
        with Session(self.engine) as session:
            session.add(self.item)
            session.commit()


class ReadItem(CRUDCommand):
    def execute(self, *args, **kwargs):
        with Session(self.engine) as session:
            return session.query(self.item.__class__).get(self.item.id)


class ReadAllItems(CRUDCommand):
    def __init__(self, item: TodoList | TodoItem | Type[TodoList] | Type[TodoItem], engine: Engine):
        if isinstance(item, type):
            item = item()

        super().__init__(item, engine)

    def execute(self, *args, **kwargs):
        with Session(self.engine) as session:
            return session.query(self.item.__class__).all()


class DeleteItem(CRUDCommand):
    def execute(self, *args, **kwargs):
        with Session(self.engine) as session:
            session.query(self.item.__class__).filter_by(id=self.item.id).delete()
            session.commit()


class UpdateItem(CRUDCommand):
    def execute(self, *args, **kwargs):
        with Session(self.engine) as session:
            session.merge(self.item)
            session.commit()



