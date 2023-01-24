import os
import flet as ft
from flet.auth.oauth_provider import OAuthProvider

def main(page: ft.Page):

    provider: OAuthProvider = OAuthProvider(
        client_id="test-client",
        client_secret="dfvYemArMX2Ca8udEzn94eOurae6dxVv",
        authorization_endpoint="https://auth.astrosync.ru/auth/realms/Test/protocol/openid-connect/auth",
        token_endpoint="https://auth.astrosync.ru/auth/realms/Test/protocol/openid-connect/token",
        redirect_url="http://localhost:8085/api/oauth/redirect",
        user_endpoint="https://auth.astrosync.ru/auth/realms/Test/protocol/openid-connect/userinfo",
        user_scopes=["email", "profile", "roles", "web-origins"],
        user_id_fn=lambda u: u["sub"]
    )

    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        if txt_number.value is not None:
            txt_number.value = str(int(txt_number.value) - 1)
            page.update()

    def plus_click(e):
        if txt_number.value is not None:
            txt_number.value = str(int(txt_number.value) + 1)
            page.update()

    def login_button_click(e):
        print(page.auth)
        page.login(provider, fetch_user=True)

    def on_login(e: ft.LoginEvent):
        if not e.error:
            toggle_login_buttons()
        else:
            print(e)

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    login_button = ft.ElevatedButton("Login", on_click=login_button_click)
    logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# ft.app(target=main)  # desktop
ft.app(target=main, port=8085, view=ft.FLET_APP)  # web