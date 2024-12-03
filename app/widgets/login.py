import tkinter as tk
from tkinter import messagebox

from ..datebase import get_session
from ..queries import user_login


class LoginForm(tk.Frame):
    def __init__(self, parent, app, on_switch_to_register):
        super().__init__(parent, bg="#1a76b9")
        self.parent = parent
        self.app = app
        self.on_switch_to_register = on_switch_to_register

        # Установка центра контейнера
        self.pack(expand=True, fill="both")  # Расширение фрейма
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Основной контейнер для выравнивания содержимого
        container = tk.Frame(self, bg="#1a76b9")
        container.grid(row=0, column=0)
        container.grid_columnconfigure(0, weight=1)

        # Заголовок
        tk.Label(
            container,
            text="Авторизация",
            font=("Arial", 18),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=0, column=0, pady=20)

        # Поле для имени пользователя
        tk.Label(
            container,
            text="Имя пользователя",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=1, column=0, sticky="w", padx=20)
        self.username_entry = tk.Entry(container, width=30, font=("Arial", 14))
        self.username_entry.grid(row=2, column=0, pady=10, padx=20)

        # Поле для пароля
        tk.Label(
            container,
            text="Пароль",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=3, column=0, sticky="w", padx=20)
        self.password_entry = tk.Entry(container, show="*", width=30, font=("Arial", 14))
        self.password_entry.grid(row=4, column=0, pady=10, padx=20)

        # Кнопка авторизации
        tk.Button(
            container,
            text="Войти",
            bg="#ffffff",
            font=("Arial", 14),
            command=self.login,
            height=1,  # Высота кнопки
            width=20,  # Ширина кнопки
        ).grid(row=5, column=0, pady=20)

        # Текст для перехода к регистрации
        link = tk.Label(
            container,
            text="У вас еще нет аккаунта? Зарегистрируйтесь",
            bg="#1a76b9",
            fg="#ffffff",
            font=("Arial", 12, "underline"),
            cursor="hand2",
        )
        link.grid(row=6, column=0, pady=10)
        link.bind("<Button-1>", lambda e: self.on_switch_to_register())

    def login(self):
        """Обрабатывает авторизацию пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Ошибка", "Введите имя пользователя и пароль!")
            return

        user, msg = user_login(get_session(), login=username, password=password)

        if user:
            messagebox.showinfo("Авторизация", msg)
            self.on_login_success(app=self.app, user=user)
        else:
            messagebox.showerror("Ошибка авторизации", msg)

    def on_login_success(self, app, user):
        """Обновляем интерфейс после успешной авторизации"""

        # Удаляем старый navbar
        if hasattr(app, "navbar") and app.navbar.winfo_exists():
            app.navbar.destroy()

        # Обновляем данные пользователя
        app.user = user  # Сохраняем данные пользователя

        # Пересоздаем navbar
        app.create_navbar(user)

        # Удаляем содержимое основного контента
        for widget in app.content_frame.winfo_children():
            widget.destroy()

        # Переупорядочиваем основные виджеты
        app.navbar.pack_forget()
        app.content_frame.pack_forget()

        app.navbar.pack(side=tk.TOP, fill=tk.X)  # Navbar всегда наверху
        app.content_frame.pack(
            side=tk.TOP, fill=tk.BOTH, expand=True
        )  # Контент в центре

        # Перезагружаем основной контент
        app.event_app.show_events()
