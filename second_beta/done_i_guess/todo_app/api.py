import uvicorn
from fastapi import FastAPI

from todo_app.crud_logic import ReadAllItems, ReadAllItemsWithCondition, DeleteItem, CreateItem, UpdateItem
from todo_app.models import TodoList, TodoItem, TodoListSchema, TodoItemSchema
from todo_app.db_utils import database


app = FastAPI()


@app.get("/lists")
def get_lists():
    return ReadAllItems(TodoList, database).execute()

@app.put("/lists")
def create_todo_list(todo_list: TodoListSchema):
    new_item = TodoList(**todo_list.dict())
    CreateItem(new_item, database).execute()
    return {"message": "List created successfully"}


@app.get("/lists/{list_id}")
def get_list(list_id: int):
    return ReadAllItemsWithCondition(TodoItem, database).execute(
        list_id=list_id
    )


@app.put("/lists/{list_id}")
def add_todo_item_to_list(list_id: int, item: TodoItemSchema):
    todo_list = next(filter(lambda i: i.id == list_id, ReadAllItems(TodoList, database).execute()), None)
    if todo_list:
        item_to_create = TodoItem(**item.dict(), todolist_id=list_id)
        CreateItem(item_to_create, database).execute()
    else:
        return {"message": "List not found"}
    return {"message": "Item added successfully"}


@app.delete("/lists/{list_id}/items/{item_id}")
def delete_todo_item_from_list(list_id: int, item_id: int):
    todo_list = ReadAllItemsWithCondition(TodoItem, database).execute(
        list_id=list_id
    )
    item = next(filter(lambda i: i.id == item_id, todo_list), None)
    if item:
        DeleteItem(item, database).execute()
        return {"message": "Item deleted successfully"}
    return {"message": "Item not found"}


@app.post("/lists/{list_id}/items/{item_id}")
def update_item(list_id: int, item_id: int, todo_item: TodoItemSchema):
    todo_list = ReadAllItemsWithCondition(TodoItem, database).execute(
        list_id=list_id
    )
    item = next(filter(lambda i: i.id == item_id, todo_list), None)
    if item:
        if item.description != todo_item.description and todo_item.description:
            item.description = todo_item.description
        if item.priority != todo_item.priority and todo_item.priority:
            item.priority = todo_item.priority
        if item.done != todo_item.done and todo_item.done:
            item.done = todo_item.done
        UpdateItem(item, database).execute()
        return {"message": "Item updated successfully"}
    return {"message": "Item not found"}


def run_app():
    uvicorn.run("api:app", port=5000, log_level="info")


if __name__ == '__main__':
    uvicorn.run("api:app", port=5000, log_level="info")
