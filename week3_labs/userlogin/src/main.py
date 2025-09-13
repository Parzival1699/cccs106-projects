import flet as ft
import mysql.connector
from db_connection import connect_db


def main(page: ft.Page):
    # Window / page config
    page.title = "User Login"
    page.window_width = 400
    page.window_height = 350
    page.window_frameless = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # --- Controls ---
    title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
    )

    username = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        width=300,
        autofocus=True,
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    password = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    # --- Dialogs ---
    success_dialog = ft.AlertDialog(
        title=ft.Text("Login Successful"),
        content=ft.Text("Welcome!"),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        icon=ft.Icons.CHECK_CIRCLE,
        icon_color=ft.Colors.GREEN,
    )

    failure_dialog = ft.AlertDialog(
        title=ft.Text("Login Failed"),
        content=ft.Text("Invalid username or password"),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        icon=ft.Icons.ERROR,
        icon_color=ft.Colors.RED,
    )

    invalid_input_dialog = ft.AlertDialog(
        title=ft.Text("Input Error"),
        content=ft.Text("Please enter username and password"),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        icon=ft.Icons.INFO,
        icon_color=ft.Colors.BLUE,
    )

    database_error_dialog = ft.AlertDialog(
        title=ft.Text("Database Error"),
        content=ft.Text("An error occurred while connecting to the database"),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        icon=ft.Icons.WARNING,
        icon_color=ft.Colors.RED,
    )

    # --- Helper to show dialogs ---
    def show_dialog(dlg: ft.AlertDialog):
        page.dialog = dlg
        dlg.open = True
        page.update()

    # --- Login logic ---
    def login_click(e):
        u, p = username.value.strip(), password.value.strip()
        if not u or not p:
            show_dialog(invalid_input_dialog)
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (u, p)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                success_dialog.content.value = f"Welcome, {u}!"
                show_dialog(success_dialog)
            else:
                show_dialog(failure_dialog)

        except Exception as err:  # catches DB errors too
            database_error_dialog.content.value = f"Database Error: {err}"
            show_dialog(database_error_dialog)

    # --- Login button ---
    login_button = ft.ElevatedButton(
        text="Login",
        width=100,
        icon=ft.Icons.LOGIN,
        on_click=login_click,
    )

    # --- Layout ---
    page.add(
        title,
        ft.Container(
            content=ft.Column([username, password], spacing=20),
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(left=0, top=20, right=40, bottom=0),
        ),
    )


ft.app(target=main)
