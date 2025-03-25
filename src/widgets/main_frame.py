import flet as ft
from threading import Thread
import api


class MainFrame(ft.Container):
    def __init__(self):
        super().__init__()

        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.padding = ft.padding.all(20)
        self.border_radius = 10

        self.video = api.Video()

        self.build()

    def build(self) -> None:
        self.title_video = ft.Text(
            self.video.title,
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        self.author_video = ft.Text(
            self.video.author,
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            overflow=ft.TextOverflow.FADE,
        )

        self.image_video = ft.Image(self.video.thumbnail, width=250)

        self.entry_search = ft.TextField(
            label="URL",
            expand=True,
            on_submit=lambda _: self.search_video(),
        )

        self.download_button = ft.FilledButton(
            "Download",
            icon=ft.icons.SAVE,
            disabled=True,
            expand=True,
            width=500,
            on_click=lambda _: Thread(target=self.download_video).run(),
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.PRIMARY_CONTAINER,
                    padding=ft.padding.all(10),
                    border_radius=10,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.image_video,
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.VIDEOCAM),
                                            self.title_video,
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.PERSON_SHARP),
                                            self.author_video,
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                ),
                ft.Row([self.entry_search]),
                self.download_button,
            ],
        )

    def download_video(self) -> None:
        download_path = self.page.client_storage.get("DOWNLOAD_PATH")
        api.download_video(self.video.url, download_path)

    def update_info(self) -> None:
        self.title_video.value = self.video.title
        self.author_video.value = self.video.author
        self.image_video.src = self.video.thumbnail

        self.download_button.disabled = False if self.entry_search.value != "" else True
        self.update()

    def search_video(self) -> None:
        url = (
            self.entry_search.value if self.entry_search.value != "" else self.video.url
        )

        self.video = api.query_video(url)
        self.update_info()
