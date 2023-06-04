from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from sqlalchemy import Engine
from kivymd.uix.boxlayout import MDBoxLayout

from todo_app.crud_logic import CreateItem
from todo_app.models import TodoList
from todo_app.screens.common import BaseMenu


class AddTodoList(Popup):
    def __init__(self, database: Engine,  **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.5)
        self.database = database
        self.text_input = MDTextField(hint_text="Wpisz nazwę listy", font_size=20, multiline=False)

        self.box = MDBoxLayout(orientation='vertical', spacing=10, padding=10)
        btn1 = MDFillRoundFlatIconButton(
            text="Dodaj",
            icon='content-save',
            size_hint=(1, None),
            on_press=lambda _: self.add_item()
        )
        btn2 = MDFillRoundFlatIconButton(
            text="Anuluj",
            icon='cancel',
            size_hint=(1, None),
            on_press=lambda _: self.dismiss()
        )

        self.box.add_widget(self.text_input)
        self.box.add_widget(btn1)
        self.box.add_widget(btn2)
        self.add_widget(self.box)

    def add_item(self):
        CreateItem(TodoList(name=self.text_input.text), self.database).execute()
        self.box.clear_widgets()
        self.box.add_widget(MDLabel(text="Dodano listę zadań"))
        self.box.add_widget(MDFillRoundFlatIconButton(
            text="OK",
            icon='check',
            size_hint=(1, None),
            on_press=lambda _: self.dismiss()
        ))

class TodoListsScreen(Screen):
    def __init__(self, database: Engine,  **kwargs):
        super().__init__(**kwargs)
        self.database = database

        base_menu = BaseMenu(
            items_type='listę zadań',
            add_action=lambda _: self.add_item(),
            del_action=lambda _: print("del"),
            mod_action=lambda _: print("mod"),
        )
        self.add_widget(base_menu)

    def add_item(self):
        AddTodoList(self.database, title='Dodaj listę zadań').open()

