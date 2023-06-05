from typing import Callable

from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout


class BaseMenu(MDBoxLayout):
    def __init__(
        self,
        items_type: str,
        add_action: Callable,
        del_action: Callable,
        mod_action: Callable,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.minimal_height = 100
        self.padding = [10, 10, 10, 10]
        self.spacing = 50

        self.add_widget(
            Button(text=f'Dodaj \n{items_type}', halign='center', on_press=add_action),
        )
        self.add_widget(
            Button(text=f'Usuń \n{items_type}', halign='center', on_press=del_action)
        )
        self.add_widget(
            Button(text=f'Modifikuj \n{items_type}', halign='center', on_press=mod_action)
        )
