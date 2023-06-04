import os

from sqlalchemy import create_engine

from todo_app.models import Base

database = create_engine('sqlite:///todo_app.db')
try:
    os.stat('todo_app.db')
except FileNotFoundError:
    Base.metadata.create_all(database)

