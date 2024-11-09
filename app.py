import flet as ft
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def main(page: ft.Page):
    init_db()
    page.window_width = 800
    page.window_height = 600
    page.title = "Sistema de Login"
    
    def login(e):
        email = login_email_field.value
        password = login_password_field.value

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            page.clean()
            page.add(
                ft.Container(
                    content=ft.Text("Bem-vindo à página inicial!", color="#000000", size=30),
                    alignment=ft.alignment.center
                )
            )
            page.update()
        else:
            login_message.value = "Email ou senha inválidos."
            login_message.color = "red"
            page.update()

    def register(e):
        name = reg_name_field.value
        email = reg_email_field.value
        password = reg_password_field.value
        address = reg_address_field.value

        if not (name and email and password and address):
            reg_message.value = "Todos os campos são obrigatórios."
            reg_message.color = "red"
            page.update()
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password, address) VALUES (?, ?, ?, ?)",
                           (name, email, password, address))
            conn.commit()
            reg_message.value = "Registro realizado com sucesso!"
            reg_message.color = "green"
            reg_name_field.value = ""
            reg_email_field.value = ""
            reg_password_field.value = ""
            reg_address_field.value = ""
        except sqlite3.IntegrityError:
            reg_message.value = "Email já cadastrado."
            reg_message.color = "red"
        finally:
            conn.close()
            page.update()

    def show_register(e):
        main_container.content = register_container
        page.update()

    def show_login(e):
        main_container.content = login_container
        page.update()

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    # Componentes do Login
    login_title = ft.Text("Login", size=30, weight="bold")
    login_email_field = ft.TextField(label="Email", width=300, border_radius=8, filled=True)
    login_password_field = ft.TextField(label="Senha", password=True, width=300, border_radius=8, filled=True)
    login_button = ft.ElevatedButton(text="Entrar", on_click=login, width=300, height=45)
    login_message = ft.Text("", size=14)
    register_link = ft.TextButton("Não tem uma conta? Registre-se", on_click=show_register)

    # Componentes do Registro
    reg_title = ft.Text("Registro", size=30, weight="bold")
    reg_name_field = ft.TextField(label="Nome", width=300, border_radius=8, filled=True)
    reg_email_field = ft.TextField(label="Email", width=300, border_radius=8, filled=True)
    reg_password_field = ft.TextField(label="Senha", password=True, width=300, border_radius=8, filled=True)
    reg_address_field = ft.TextField(label="Endereço", width=300, border_radius=8, filled=True)
    register_button = ft.ElevatedButton(text="Registrar", on_click=register, width=300, height=45)
    reg_message = ft.Text("", size=14)
    login_link = ft.TextButton("Já tem uma conta? Faça login", on_click=show_login)

    # Container do Login
    login_container = ft.Container(
        content=ft.Column(
            [login_title, login_email_field, login_password_field, login_button, login_message, register_link],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
    )

    # Container do Registro
    register_container = ft.Container(
        content=ft.Column(
            [reg_title, reg_name_field, reg_email_field, reg_password_field, reg_address_field, 
             register_button, reg_message, login_link],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
    )

    # Botão de tema
    theme_button = ft.IconButton(icon=ft.icons.BRIGHTNESS_6, on_click=toggle_theme)
    theme_container = ft.Container(
        content=theme_button,
        padding=10,
        alignment=ft.alignment.top_right
    )

    # Container principal que vai conter todas as telas
    main_container = ft.Container(
        content=login_container,
        expand=True,
        alignment=ft.alignment.center
    )

    # Layout final da página
    page.add(
        ft.Stack([
            main_container,
            theme_container
        ])
    )

    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

ft.app(target=main)
