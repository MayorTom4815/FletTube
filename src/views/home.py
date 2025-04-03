import flet as ft
from widgets import MainFrame


class Home(ft.View):
    def __init__(self) -> None:
        super().__init__()

        self.appbar = ft.AppBar(
            leading=ft.Image("icon.png"),
            title=ft.Text("FletTube"),
            actions=[ft.IconButton(ft.Icons.SETTINGS, on_click=self.settings_go)],
        )
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.build()

    def settings_go(self, e) -> None:
        self.page.go("/settings")

    def build(self) -> None:
        self.controls = [MainFrame()]
