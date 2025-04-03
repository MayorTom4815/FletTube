import flet as ft
from threading import Thread
import api


class MainFrame(ft.Container):
    def __init__(self):
        super().__init__()

        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.padding = ft.padding.all(20)
        self.border_radius = 10
        self.width = 600

        self.video = api.Video()

    def build(self) -> None:
        self.download_alert = ft.AlertDialog(
            title=ft.Text("Download..."), content=ft.ProgressBar(expand=True)
        )

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
            label="YouTube URL video",
            prefix_icon=ft.Icons.LINK,
            expand=True,
            on_submit=lambda _: self.search_video(),
        )

        self.download_button = ft.FilledButton(
            "Download",
            icon=ft.Icons.SAVE,
            disabled=True,
            expand=True,
            width=500,
            on_click=self.download_video,
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
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
                                            ft.Icon(ft.Icons.VIDEOCAM),
                                            self.title_video,
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PERSON_SHARP),
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

    def download_video(self, e) -> None:
        self.page.open(self.download_alert)

        download_path = self.page.client_storage.get("DOWNLOAD_PATH")
        only_sound = self.page.client_storage.get("ONLY_SOUND")

        action = Thread(api.download_video(self.video.url, download_path, only_sound))
        action.run()

        if not action.is_alive():
            self.page.close(self.download_alert)

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
