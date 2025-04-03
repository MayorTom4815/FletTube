import flet as ft


class Title(ft.Text):
    def __init__(self, title: str) -> None:
        super().__init__()

        self.theme_style = ft.TextThemeStyle.TITLE_LARGE
        self.weight = ft.FontWeight.BOLD

        self.value = title


class ConfigDescription(ft.Text):
    def __init__(self, text: str) -> None:
        super().__init__()

        self.theme_style = ft.TextThemeStyle.TITLE_MEDIUM
        self.weight = ft.FontWeight.BOLD

        self.value = text


class ConfigSection(ft.Container):
    def __init__(self, controls: list) -> None:
        super().__init__()

        self.bgcolor = ft.Colors.PRIMARY_CONTAINER
        self.padding = ft.padding.all(20)
        self.border_radius = 10

        self.width = 600

        self.content = ft.Column(controls, spacing=20)


class Config(ft.Row):
    def __init__(self, controls: list) -> None:
        super().__init__()

        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.controls = controls


class Configs(ft.View):
    def __init__(self) -> None:
        super().__init__()

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_LEFT, on_click=lambda _: self.page.go("/")
            ),
            title=ft.Text("Settings"),
        )

    def redifine_download_path(self, e) -> None:
        file_picker: ft.FilePicker = self.page.overlay[0]
        file_picker.get_directory_path()

    def get_dropdown_options(self) -> list:
        colors = [
            ft.Colors.BLUE,
            ft.Colors.RED,
            ft.Colors.GREEN,
            ft.Colors.YELLOW,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.TEAL,
        ]

        options = []

        for item in colors:
            options.append(ft.dropdown.Option(item.value))

        return options

    def dropdown_color_select(self, e):
        self.page.client_storage.set("COLOR_UI", e.data)

        color_selected = self.page.client_storage.get("COLOR_UI")
        self.page.theme = ft.Theme(color_scheme_seed=color_selected)

        self.page.update()

    def change_only_audio(self, e) -> None:
        value = True if e.data == "true" else False
        self.page.client_storage.set("ONLY_SOUND", value)

    def build(self) -> None:
        self.button_redifine = ft.FilledButton(
            "Select",
            icon=ft.Icons.SELECT_ALL,
            on_click=self.redifine_download_path,
        )

        self.dropdown_color = ft.Dropdown(
            filled=True,
            label="Colors",
            options=self.get_dropdown_options(),
            on_change=self.dropdown_color_select,
        )

        self.switch_music = ft.Switch(
            value=self.page.client_storage.get("ONLY_SOUND"),
            on_change=self.change_only_audio,
        )

        self.controls = [
            ConfigSection(
                [
                    ft.Row([ft.Icon(ft.Icons.COLOR_LENS), Title("UI")]),
                    Config(
                        [
                            ConfigDescription("Change color scheme: "),
                            self.dropdown_color,
                        ]
                    ),
                ]
            ),
            ConfigSection(
                [
                    ft.Row([ft.Icon(ft.Icons.DOWNLOAD), Title("Downloads")]),
                    Config(
                        [
                            ConfigDescription("Change download directory:"),
                            self.button_redifine,
                        ]
                    ),
                    Config(
                        [
                            ConfigDescription("Download only video sound:"),
                            self.switch_music,
                        ]
                    ),
                ]
            ),
        ]
