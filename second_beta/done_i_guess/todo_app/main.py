#!/usr/bin/env python3
import sys
import os
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from todo_app.api import run_app
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from sqlalchemy import Engine

from todo_app.screens.todo_lists import TodoListsScreen
from todo_app.db_utils import database


class MainApp(MDApp):
    def __init__(self, db: Engine, **kwargs):
        super().__init__(**kwargs)
        self.database = db

    def build(self):
        sm = ScreenManager()
        sm.add_widget(TodoListsScreen(self.database), name="todo_lists")
        return sm

if __name__ == '__main__':
    threading.Thread(target=run_app, daemon=True).start()
    MainApp(database).run()
    exit(0)
