from typing import List

from todo_app.models import TodoItem


def sort_by_status(items: List[TodoItem]) -> list:
    items.sort(key=lambda item: item.done)
    return items


def sort_by_priority(items: List[TodoItem]) -> list:
    items.sort(key=lambda item: item.priority)
    items.reverse()
    return items


def sort_by_name(items: List[TodoItem]) -> list:
    items.sort(key=lambda item: item.description)
    return items
