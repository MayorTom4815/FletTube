import flet as ft
import views


def main(page: ft.Page) -> None:
    def initializate() -> None:
        if not page.client_storage.contains_key("COLOR_UI"):
            page.client_storage.set("COLOR_UI", "blue")

        if not page.client_storage.contains_key("ONLY_SOUND"):
            page.client_storage.set("ONLY_SOUND", True)

        color = page.client_storage.get("COLOR_UI")
        page.theme = ft.Theme(color_scheme_seed=color)

    dialog_permission_request = ft.AlertDialog(
        title=ft.Text("Download path don´t found"),
        content=ft.Text("Please select a directory, where we can download videos."),
        modal=True,
        actions=[
            ft.FilledButton(
                text="Select directory",
                icon=ft.Icons.SELECT_ALL,
                on_click=lambda _: file_picker.get_directory_path(),
            )
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "FletTube"

    page.window.height = 600
    page.window.width = 800
    page.padding = ft.padding.all(20)

    def dir_picked(e) -> None:
        page.client_storage.set("DOWNLOAD_PATH", e.path)

        if page.route == "/":
            page.close(dialog_permission_request)

    file_picker = ft.FilePicker(on_result=dir_picked)
    page.overlay.append(file_picker)

    def on_change_views(e) -> None:
        troute = ft.TemplateRoute(page.route)
        page.views.pop()

        if troute.match("/"):
            initializate()

            if not page.client_storage.contains_key("DOWNLOAD_PATH"):
                page.open(dialog_permission_request)

            page.views.append(views.Home())

        elif troute.match("/settings"):
            page.views.append(views.Configs())

        page.update()

    def on_pop_view(e) -> None:
        page.views.clear()
        page.go(page.views[-1].route)

    page.on_view_pop = on_pop_view
    page.on_route_change = on_change_views

    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
