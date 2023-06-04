from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from todo_app.crud_logic import CreateItem, ReadAllItems, DeleteItem, ReadAllItemsWithCondition
from todo_app.models import TodoList, TodoItem
from todo_app.screens.todo_list_items import TodoListScreen


class AddTodoList(Popup):
    def __init__(self, database: Engine, callback=None, **kwargs):
        super().__init__(**kwargs)

        self.callback = callback

        def check_text_field(text_field):
            if text_field.text:
                return True
            text_field.helper_text = "Pole nie może być puste"
            text_field.error = True
            return False

        self.background_color = (0.1, 0.1, 0.1, 0.4)
        self.size_hint = (1, 0.5)
        self.database = database
        self.text_input = MDTextField(
            hint_text="Wpisz nazwę listy",
            font_size=20,
            multiline=False,
            size_hint=(1, None),
            helper_text_mode="on_error",
            text_color_normal=(1, 1, 1, 1),
        )

        self.box = MDBoxLayout(orientation='vertical', spacing=10, padding=10)
        btn1 = MDFillRoundFlatIconButton(
            text="Dodaj",
            icon='content-save',
            size_hint=(1, None),
            on_press=lambda _: self.add_item() if check_text_field(self.text_input) else None
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
        try:
            CreateItem(TodoList(name=self.text_input.text.strip()), self.database).execute()
        except IntegrityError:
            self.text_input.helper_text = "Lista o takiej nazwie już istnieje!"
            self.text_input.error = True
            return

        self.box.clear_widgets()
        if self.callback:
            self.callback()
        self.dismiss()


class RemoveList(Popup):
    def __init__(self, database: Engine, item: TodoList, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.todo_list = item
        self.background_color = (0.1, 0.1, 0.1, 1)
        self.size_hint = (1, 0.5)
        self.database = database
        self.box = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        self.box.add_widget(MDLabel(
            text=f"Czy na pewno chcesz usunąć listę {item.name}?",
            font_size=20,
            halign='center',
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))
        self.box.add_widget(MDFillRoundFlatIconButton(
            text="Usuń listę",
            icon='delete',
            size_hint=(1, None),
            on_press=lambda _: self.remove_item()
        ))
        self.box.add_widget(MDFillRoundFlatIconButton(
            text="Anuluj",
            icon='cancel',
            size_hint=(1, None),
            on_press=lambda _: self.dismiss()
        )
)
        self.add_widget(self.box)

    def remove_item(self):
        DeleteItem(self.todo_list, self.database).execute()
        if self.callback:
            self.callback()
        self.dismiss()


class TodoListsScreen(Screen):
    def __init__(self, database: Engine, **kwargs):
        super().__init__(**kwargs)
        self.name = 'todo_lists'
        self.database = database
        self.items = []

        add_list_button = MDFillRoundFlatIconButton(
            text="Dodaj listę zadań",
            size_hint=(1, None),
            on_press=lambda _: AddTodoList(self.database, title='Dodaj listę zadań', callback=self.update).open(),
        )

        root = MDScrollView(
            size=(Window.width, Window.height),
        )

        self.main_layout = MDGridLayout(cols=1, spacing=10, size_hint_y=None, height=Window.height, id="main_layout")
        self.main_layout.add_widget(MDTopAppBar(
            elevation=4,
            title="Listy zadań",
        ))
        self.main_layout.add_widget(add_list_button)
        self.items_list = MDList(
            id="md_list",
        )

        self.main_layout.add_widget(self.items_list)
        root.add_widget(self.main_layout)
        self.add_widget(root)
        self.update()

    def remove_list(self, item):
        DeleteItem(item, self.database).execute()
        self.update()

    def update_items(self):
        self.items = ReadAllItems(TodoList, self.database).execute()
        if len(self.items) > 5:
            self.main_layout.height = Window.height + 64 * (len(self.items) - 4)

    def update(self):
        self.items_list.clear_widgets()
        self.update_items()
        for idx, item in enumerate(self.items):
            items = ReadAllItemsWithCondition(TodoItem, self.database).execute(
                todo_list=item
            )
            done_items = [i for i in items if i.done]
            description = f'Ilość zadań {len(items)}'
            if len(items) > 0:
                description += f', zrobione {len(done_items)}'

            self.items_list.add_widget(
                ThreeLineAvatarIconListItem(
                    IconRightWidget(
                        id=str(idx),
                        icon="minus",
                        on_press=lambda button: RemoveList(
                            self.database,
                            title='Usuń listę zadań',
                            item=self.items[int(button.id)],
                            callback=self.update
                        ).open()
                    ),
                    id=str(idx),
                    text=item.name,
                    secondary_text=description,
                    on_press=lambda button: self.manager.switch_to(
                        TodoListScreen(self.database, self.items[int(button.id)], self)
                    )
                )
            )
