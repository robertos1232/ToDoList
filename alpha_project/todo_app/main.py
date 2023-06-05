#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from sqlalchemy import create_engine, Engine

from todo_app.models import Base

from todo_app.screens.todo_lists import TodoListsScreen


class MainApp(MDApp):
    def __init__(self, database: Engine, **kwargs):
        super().__init__(**kwargs)
        self.database = database

    def build(self):
        sm = ScreenManager()
        sm.add_widget(TodoListsScreen(self.database))
        return sm


if __name__ == '__main__':
    db_engine = create_engine('sqlite:///todo_app.db')

    try:
        os.stat('todo_app.db')
    except FileNotFoundError:
        Base.metadata.create_all(db_engine)

    MainApp(db_engine).run()
