from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, IconRightWidget, TwoLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

from todo_app.crud_logic import CreateItem, ReadAllItemsWithCondition, UpdateItem, DeleteItem
from todo_app.models import TodoItem, TodoList, Priority
from todo_app.utils import sort_by_status, sort_by_priority, sort_by_name


def get_color(priority: int):
    case = {
        1: (0.2, 0.8, 0.2, 1),
        2: (0.8, 0.8, 0.2, 1),
        3: (0.8, 0.0, 0.0, 1)
    }
    return case.get(priority, (1, 1, 1, 1))


def check_text_field(text_field):
    if text_field.text:
        return True
    text_field.helper_text = "Pole nie może być puste"
    text_field.error = True
    return False


class AddModifyTodoItem(Popup):
    def __init__(self, database: Engine, todo_list: TodoList, todo_item=None, callback=None, **kwargs):

        super().__init__(**kwargs)

        self.title = "Dodaj zadanie"
        self.callback = callback
        self.todo_list = todo_list
        self.background_color_theme = "Custom"
        self.background_color = (10, 10, 10, 1)
        self.size_hint = (1, 1)
        self.width_offset = Window.width * 0.8
        self.database = database
        self.priority = Priority.NON.value
        self.task_description = MDTextField(
            hint_text="Wpisz opis zadania",
            font_size=20,
            multiline=False,
            size_hint=(1, None),
            helper_text_mode="on_error",
            required=True,

        )
        self.todo_item = todo_item
        self.action = self.update_item if self.todo_item else self.add_item
        if self.todo_item:
            self.task_description.text = todo_item.description
            self.priority = todo_item.priority
            self.title = "Edytuj zadanie"

        self.box = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        btn1 = MDFillRoundFlatIconButton(
            text="Dodaj",
            icon='content-save',
            size_hint=(1, None),
            on_press=lambda _: self.execute() if check_text_field(self.task_description) else None
        )
        btn2 = MDFillRoundFlatIconButton(
            text="Anuluj",
            icon='cancel',
            size_hint=(1, None),
            on_press=lambda _: self.dismiss()
        )
        self.box.add_widget(self.task_description)
        priority_items = MDGridLayout(cols=2, spacing=10, size_hint=(1, None), height=200)

        priority_items.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    MDCheckbox(
                        active=True if self.priority == Priority.HIGH.value else False,
                        group="priority",
                        on_press=lambda _: setattr(self, 'priority', Priority.HIGH.value)
                    ),
                ),
                text="Wysoki",
            )
        )
        priority_items.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    MDCheckbox(
                        active=True if self.priority == Priority.MEDIUM.value else False,
                        group="priority",
                        on_press=lambda _: setattr(self, 'priority', Priority.MEDIUM.value)
                    ),
                ),
                text="Średni",
            )
        )
        priority_items.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    MDCheckbox(
                        active=True if self.priority == Priority.LOW.value else False,
                        group="priority",
                        on_press=lambda _: setattr(self, 'priority', Priority.LOW.value)
                    ),
                ),
                text="Niski",
            )
        )
        priority_items.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    MDCheckbox(
                        active=True if self.priority == Priority.NON.value else False,
                        group="priority",
                        on_press=lambda _: setattr(self, 'priority', Priority.NON.value)
                    ),
                ),
                text="Brak",
            )
        )

        self.box.add_widget(priority_items)
        self.box.add_widget(btn1)
        self.box.add_widget(btn2)
        self.add_widget(self.box)

    def update_item(self):
        UpdateItem(
            TodoItem(
                id=self.todo_item.id,
                description=self.task_description.text.strip(),
                todolist_id=self.todo_list.id,
                priority=self.priority
            ),
            self.database
        ).execute()

    def add_item(self):
        CreateItem(
            TodoItem(
                description=self.task_description.text.strip(),
                todolist_id=self.todo_list.id,
                priority=self.priority
            ),
            self.database
        ).execute()

    def execute(self):
        try:
            self.action()
        except IntegrityError:
            self.task_description.helper_text = "Lista o takiej nazwie już istnieje!"
            self.text_input.error = True
            return
        self.box.clear_widgets()
        if self.callback:
            self.callback()
        self.dismiss()


class TodoListScreen(Screen):

    def __init__(self, database: Engine, todo_list: TodoList, todo_lists_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'todo_list'
        self.database = database
        self.todo_list = todo_list
        self.items = []
        self.todo_list_manager = todo_lists_manager
        self.sort_type = "status"

        button_layout = MDGridLayout(cols=2, spacing=10, size_hint_y=None, height=40, id="button_layout")
        button_layout.add_widget(
            MDFillRoundFlatIconButton(
                text="Dodaj nowe zadanie",
                size_hint=(1, None),
                on_press=lambda _: AddModifyTodoItem(self.database, todo_list, callback=self.update).open()
            )
        )

        button_layout.add_widget(
            MDFillRoundFlatIconButton(
                text="Usuń wykonane zadania",
                size_hint=(1, None),
                on_press=lambda _: self.remove_done_items(),
                md_bg_color="red"
            )
        )
        search_layout = MDGridLayout(cols=2, spacing=10, size_hint_y=None, height=40, id="search_filter_layout")
        self.dropdown_menu_caller = MDFillRoundFlatIconButton(
            text="Sortuj",
            size_hint=(0.5, None),
            on_release=lambda _: self.dropdown_menu.open()
        )
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Status",
                "on_release": lambda: self.set_sort_type("status")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Priorytet",
                "on_release": lambda: self.set_sort_type("priority")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Nazwa",
                "on_release": lambda: self.set_sort_type("name")
            },
        ]

        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_menu_caller,
            items=menu_items,
            width_mult=4,
            max_height=Window.height / 4,
        )

        self.search_items = MDTextField(
            mode="round",
            hint_text="Szukaj",
            size_hint=(1, None),
            height=40,
            width=200,
            icon_right="search",
            on_text_validate=self.update,
            on_text=self.update
        )

        search_layout.add_widget(self.search_items)
        search_layout.add_widget(self.dropdown_menu_caller)

        root = MDScrollView(
            size=(Window.width, Window.height),
        )

        self.main_layout = MDGridLayout(cols=1, spacing=10, size_hint_y=None, height=Window.height, id="main_layout")
        self.main_layout.add_widget(MDTopAppBar(
            elevation=4,
            title=f"Lista zadań: {todo_list.name}",
            on_press=lambda _: self.manager.current == 'todo_lists',
            on_press_back_button=lambda _: self.manager.current == 'todo_lists',
            right_action_items=[["backburger", lambda _: self.back_to_menu()]]
        ))
        self.main_layout.add_widget(button_layout)
        self.main_layout.add_widget(search_layout)
        self.items_list = MDList(
            id="md_list",
        )

        self.main_layout.add_widget(self.items_list)
        root.add_widget(self.main_layout)
        self.add_widget(root)
        self.update()

    def update(self, *args):
        self.update_items()
        self.items_list.clear_widgets()
        for idx, item in enumerate(self.items):
            self.items_list.add_widget(
                TwoLineAvatarIconListItem(
                    IconLeftWidget(
                        id=str(idx),
                        icon="circle",
                        theme_text_color="Custom",
                        text_color=get_color(item.priority),

                    ),
                    IconRightWidget(
                        MDCheckbox(
                            active=item.done,
                            id=str(idx),
                            on_press=lambda button: self.update_status(self.items[int(button.id)]),
                            unselected_color=(0, 1, 0, 1),
                        ),
                    ),
                    id=str(idx),
                    text=item.description,
                    on_press=lambda button: AddModifyTodoItem(
                        self.database,
                        self.todo_list,
                        self.items[int(button.id)],
                        self.update
                    ).open(),
                )
            )

    def update_items(self):
        self.items = ReadAllItemsWithCondition(TodoItem, self.database).execute(
            todo_list=self.todo_list
        )
        if len(self.items) > 6:
            self.main_layout.height = Window.height + 48 * (len(self.items) - 5)

        match self.sort_type:
            case "status":
                self.items = sort_by_status(self.items)
            case "priority":
                self.items = sort_by_priority(self.items)
            case "name":
                self.items = sort_by_name(self.items)
        if self.search_items.text:
            self.items = list(
                filter(lambda item: self.search_items.text.lower() in item.description.lower(), self.items)
            )
        return list(self.items)

    def update_status(self, item: TodoItem):
        item.done = not item.done
        UpdateItem(item, self.database).execute()
        self.update()

    def remove_done_items(self):
        for item in self.items:
            if item.done:
                DeleteItem(item, self.database).execute()
        self.update()

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type
        self.update()

    def back_to_menu(self):
        self.manager.switch_to(
            self.todo_list_manager
        )
