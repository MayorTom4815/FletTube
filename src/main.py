import flet as ft
from views import Home


def main(page: ft.Page) -> None:
    dialog_permission_request = ft.AlertDialog(
        title=ft.Text("Download path don´t found"),
        content=ft.Text("Please select a directory, where we can download videos."),
        modal=True,
        actions=[
            ft.FilledButton(
                text="Select directory",
                icon=ft.icons.SELECT_ALL,
                on_click=lambda _: file_picker.get_directory_path(),
            )
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "FletTube"

    page.window.height = 600
    page.window.width = 800
    page.padding = ft.padding.all(20)

    def dir_picked(e) -> None:
        page.client_storage.set("DOWNLOAD_PATH", e.path)
        page.close(dialog_permission_request)

    file_picker = ft.FilePicker(on_result=dir_picked)
    page.overlay.append(file_picker)

    def on_change_views(e) -> None:
        troute = ft.TemplateRoute(page.route)
        page.views.pop()

        if troute.match("/"):
            if not page.client_storage.contains_key("DOWNLOAD_PATH"):
                page.open(dialog_permission_request)

            page.views.append(Home())

        page.update()

    def on_pop_view(e) -> None:
        page.views.clear()
        page.go(page.views[-1].route)

    page.on_view_pop = on_pop_view
    page.on_route_change = on_change_views

    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
