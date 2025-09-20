# main.py
import flet as ft
import asyncio
import itertools
from database import init_db
from app_logic import display_contacts, add_contact, export_contacts_to_csv, import_contacts_from_csv

def main(page: ft.Page):
    page.title = "Contact Book"
    page.window_width = 500
    page.window_height = 750

    db_conn = init_db()

    # ✅ Animated gradient setup
    gradients = itertools.cycle([
        [ft.Colors.PINK_100, ft.Colors.PURPLE_400],
        [ft.Colors.BLUE_100, ft.Colors.CYAN_400],
        [ft.Colors.GREEN_100, ft.Colors.LIME_400],
        [ft.Colors.AMBER_100, ft.Colors.ORANGE_400],
    ])

    # Root container with gradient background
    bg_container = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=next(gradients),
        ),
        content=None,  # will hold UI later
    )

    # async loop for background animation
    async def animate_background():
        while True:
            await asyncio.sleep(3)  # 3 seconds per step
            bg_container.gradient = ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=next(gradients),
            )
            page.update()

    page.run_task(animate_background)

    # ---------------- Inputs ----------------
    def styled_textfield(label, width=400):
        return ft.TextField(
            label=label,
            width=width,
            border_radius=10,
            bgcolor=ft.Colors.GREY_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_800,
            border_color=ft.Colors.GREY_400,
        )

    name_input = styled_textfield("Name")
    phone_input = styled_textfield("Phone")
    email_input = styled_textfield("Email")
    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    search_input = styled_textfield("Search contacts...")

    search_input.on_change = lambda e: display_contacts(
        page, contacts_list_view, db_conn, search_input.value
    )

    # ---------------- Theme Toggle ----------------
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        name_input.bgcolor = phone_input.bgcolor = email_input.bgcolor = search_input.bgcolor = (
            ft.Colors.GREY_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_800
        )
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Toggle Dark/Light Mode",
        on_click=toggle_theme
    )

    # ---------------- Buttons ----------------
    button_width = 200

    def hover_effect(button, default_color, hover_color):
        def on_hover(e):
            button.bgcolor = hover_color if e.data == "true" else default_color
            button.update()
        return on_hover

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn),
        width=button_width,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
    )
    add_button.on_hover = hover_effect(add_button, ft.Colors.BLUE, ft.Colors.BLUE_700)

    export_button = ft.ElevatedButton(
        text="Export to CSV",
        on_click=lambda e: export_contacts_to_csv(page, db_conn),
        width=button_width,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
    )
    export_button.on_hover = hover_effect(export_button, ft.Colors.GREEN, ft.Colors.GREEN_700)

    import_button = ft.ElevatedButton(
        text="Import from CSV",
        on_click=lambda e: import_contacts_from_csv(page, db_conn, contacts_list_view),
        width=button_width,
        bgcolor=ft.Colors.ORANGE,
        color=ft.Colors.WHITE,
    )
    import_button.on_hover = hover_effect(import_button, ft.Colors.ORANGE, ft.Colors.ORANGE_700)

    # ---------------- Layout inside background ----------------
    bg_container.content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
                        theme_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Enter Contact Details:", size=18, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Column(
                    [export_button, import_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Divider(),
                search_input,
                ft.Text("Contacts:", size=18, weight=ft.FontWeight.BOLD),
                contacts_list_view,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.alignment.center,
        padding=20,
    )

    # Add root background container to page
    page.add(bg_container)

    # Initial load
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)
