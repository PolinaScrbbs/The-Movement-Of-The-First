import tkinter as tk
from tkinter import messagebox

from ..datebase import get_session
from ..queries import registration_user
from ..queries.schemes import UserCreate


class RegistrationForm(tk.Frame):
    def __init__(self, parent, on_switch_to_login):
        super().__init__(parent, bg="#1a76b9")
        self.on_switch_to_login = on_switch_to_login

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
            text="Регистрация",
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

        # Поле для полного имени
        tk.Label(
            container,
            text="Полное имя",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=3, column=0, sticky="w", padx=20)
        self.full_name_entry = tk.Entry(container, width=30, font=("Arial", 14))
        self.full_name_entry.grid(row=4, column=0, pady=10, padx=20)

        # Поле для пароля
        tk.Label(
            container,
            text="Пароль",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=5, column=0, sticky="w", padx=20)
        self.password_entry = tk.Entry(container, show="*", width=30, font=("Arial", 14))
        self.password_entry.grid(row=6, column=0, pady=10, padx=20)

        # Поле для подтверждения пароля
        tk.Label(
            container,
            text="Подтвердите пароль",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=7, column=0, sticky="w", padx=20)
        self.confirm_password_entry = tk.Entry(container, show="*", width=30, font=("Arial", 14))
        self.confirm_password_entry.grid(row=8, column=0, pady=10, padx=20)

        # Кнопка регистрации
        tk.Button(
            container,
            text="Зарегистрироваться",
            bg="#ffffff",
            font=("Arial", 14),
            command=self.register,
            height=1,  # Высота кнопки
            width=20,  # Ширина кнопки
        ).grid(row=9, column=0, pady=20)

        # Текст для перехода к авторизации
        link = tk.Label(
            container,
            text="Уже зарегистрированы? Авторизуйтесь",
            bg="#1a76b9",
            fg="#ffffff",
            font=("Arial", 12, "underline"),
            cursor="hand2",
        )
        link.grid(row=10, column=0, pady=10)
        link.bind("<Button-1>", lambda e: self.on_switch_to_login())

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
