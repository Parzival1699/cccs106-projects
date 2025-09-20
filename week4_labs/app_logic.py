# app_logic.py
import flet as ft
import csv
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact

        # Base shadow styles
        default_shadow = ft.BoxShadow(
            blur_radius=8,
            spread_radius=1,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(1, 2)
        )
        hover_shadow = ft.BoxShadow(
            blur_radius=12,
            spread_radius=2,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(2, 4)
        )

        # Contact card container
        contact_card = ft.Container(
            content=ft.Card(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(name, size=16, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.PHONE, size=14), ft.Text(phone or "N/A")]),
                        ft.Row([ft.Icon(ft.Icons.EMAIL, size=14), ft.Text(email or "N/A")])
                    ]),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Edit",
                                icon=ft.Icons.EDIT,
                                on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                            ),
                            ft.PopupMenuItem(
                                text="Delete",
                                icon=ft.Icons.DELETE,
                                on_click=lambda _, cid=contact_id: confirm_delete(page, cid, db_conn, contacts_list_view)
                            ),
                        ],
                    ),
                )
            ),
            shadow=default_shadow,
            border_radius=12,
            padding=10,
            margin=5,
        )

        # ✅ Add hover effect to card
        def on_hover(e, card=contact_card):
            if e.data == "true":  # mouse entered
                card.shadow = hover_shadow
            else:  # mouse left
                card.shadow = default_shadow
            card.update()

        contact_card.on_hover = on_hover

        contacts_list_view.controls.append(contact_card)

    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact with validation and refreshes the list."""
    name_input, phone_input, email_input = inputs

    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return

    add_contact_db(db_conn, name_input.value.strip(), phone_input.value.strip(), email_input.value.strip())

    for field in inputs:
        field.value = ""

    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def confirm_delete(page, contact_id, db_conn, contacts_list_view):
    """Show confirmation dialog before deleting a contact."""

    def yes_action(e):
        delete_contact_db(db_conn, contact_id)
        display_contacts(page, contacts_list_view, db_conn)  # ✅ refresh first
        page.dialog.open = False
        page.update()
        # ✅ Toast notification
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Contact deleted ✅"),
            bgcolor=ft.Colors.RED,
            open=True
        )
        page.update()

    def no_action(e):
        page.dialog.open = False
        page.update()

    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED), ft.Text("Confirm Delete", weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.START,
        ),
        content=ft.Text("This action cannot be undone. Delete this contact?", color=ft.Colors.RED_700),
        actions=[
            ft.TextButton("Cancel", on_click=no_action),
            ft.TextButton("Delete", on_click=yes_action, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog.open = True
    page.update()


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        if not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return

        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )

    page.open(dialog)


# ---------- CSV FUNCTIONS ----------

def export_contacts_to_csv(page, db_conn):
    """Exports contacts to contacts.csv"""
    contacts = get_all_contacts_db(db_conn)
    with open("contacts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Phone", "Email"])
        writer.writerows(contacts)

    page.snack_bar = ft.SnackBar(ft.Text("Contacts exported to contacts.csv"), open=True)
    page.update()


def import_contacts_from_csv(page, db_conn, contacts_list_view):
    """Imports contacts from contacts.csv"""
    try:
        with open("contacts.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                add_contact_db(db_conn, row["Name"], row["Phone"], row["Email"])
        display_contacts(page, contacts_list_view, db_conn)
        page.snack_bar = ft.SnackBar(ft.Text("Contacts imported from contacts.csv"), open=True)
    except FileNotFoundError:
        page.snack_bar = ft.SnackBar(ft.Text("contacts.csv not found!"), open=True)

    page.update()
