import tkinter as tk
from tkinter import messagebox

from ..datebase import get_session
from ..queries import registration_user
from ..queries.schemes import UserCreate


class RegistrationForm(tk.Frame):
    def __init__(self, parent, on_switch_to_login):
        super().__init__(parent)
        self.on_switch_to_login = on_switch_to_login

        self.pack(pady=20)

        # Заголовок
        tk.Label(self, text="Регистрация", font=("Arial", 18)).pack(pady=10)

        # Поле для имени пользователя
        tk.Label(self, text="Имя пользователя").pack(anchor="w", padx=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(fill="x", padx=5, pady=5)

        # Поле для полного имени
        tk.Label(self, text="Полное имя").pack(anchor="w", padx=5)
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.pack(fill="x", padx=5, pady=5)

        tk.Label(self, text="Пароль").pack(anchor="w", padx=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(fill="x", padx=5, pady=5)

        # Поле для подтверждения пароля
        tk.Label(self, text="Подтвердите пароль").pack(anchor="w", padx=5)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(fill="x", padx=5, pady=5)

        # Кнопка регистрации
        tk.Button(self, text="Зарегистрироваться", command=self.register).pack(pady=10)

        # Кнопка для перехода к авторизации
        tk.Button(
            self,
            text="Уже зарегистрированы? Авторизуйтесь",
            command=self.on_switch_to_login,
        ).pack(pady=5)

    def register(self):
        """Обрабатывает регистрацию пользователя."""
        username = self.username_entry.get()
        full_name = self.full_name_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not full_name or not password or not confirm_password:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return

        user = registration_user(
            get_session(),
            UserCreate(
                username=username,
                full_name=full_name,
                password=password,
                confirm_password=confirm_password,
            ),
        )

        messagebox.showinfo(
            "Регистрация", f"Пользователь {user.username} успешно зарегистрирован!"
        )
