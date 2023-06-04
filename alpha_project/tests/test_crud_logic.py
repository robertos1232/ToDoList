import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from todo_app.crud_logic import (
    CreateItem,
    ReadItem,
    UpdateItem,
    DeleteItem,
    ReadAllItems
)
from todo_app.models import TodoList, TodoItem, Base


@pytest.fixture(scope='session')
def engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def todo_list():
    todolist = TodoList(name='test')
    return todolist


@pytest.fixture
def engine_with_todo_list_added(engine, todo_list):
    with Session(engine) as session:
        session.add(todo_list)
        session.commit()
    return engine


@pytest.fixture
def todo_item(engine, todo_list):
    item = TodoItem(description='test', todolist_id=todo_list.id)
    return item


def test_create_item_on_todo_list_object(engine, todo_list):
    CreateItem(todo_list, engine).execute()
    with Session(engine) as session:
        items = session.query(TodoList).all()
        assert len(items) == 1
        assert items[0].name == 'test'
        assert items[0].id is not None


def test_get_item_with_todo_list_object(engine_with_todo_list_added):
    engine = engine_with_todo_list_added
    item = ReadItem(TodoList(id=1), engine).execute()
    assert item.name == 'test'
    assert item.id == 1


def test_update_item(engine_with_todo_list_added):
    engine = engine_with_todo_list_added
    item = TodoList(id=1, name='updated')

    UpdateItem(item, engine).execute()
    with Session(engine) as session:
        items = session.query(TodoList).all()
        assert len(items) == 1
        assert items[0].name == 'updated'
        assert items[0].id == 1


def test_delete_item(engine_with_todo_list_added):
    engine = engine_with_todo_list_added
    item = TodoList(id=1)
    DeleteItem(item, engine).execute()
    with Session(engine) as session:
        items = session.query(TodoList).all()
        assert len(items) == 0


def test_read_all_items(engine_with_todo_list_added):
    engine = engine_with_todo_list_added
    items = ReadAllItems(TodoList, engine).execute()
    assert len(items) == 1
    assert items[0].name == 'test'
    assert items[0].id == 1
