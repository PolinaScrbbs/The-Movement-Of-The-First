import tkinter as tk
from tkinter import messagebox
from .base import BaseApp
from .registration import RegistrationForm


class App(BaseApp):
    def __init__(self):
        # Передаем token=None, чтобы кнопка "Войти" была видимой
        super().__init__(token=None)

    def show_login_form(self):
        """Показываем форму для авторизации"""
        # Удаляем старое содержимое
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Заголовок формы
        tk.Label(self.content_frame, text="Авторизация", font=("Arial", 18)).pack(
            pady=10
        )

        # Поле для имени пользователя
        tk.Label(self.content_frame, text="Имя пользователя").pack(anchor="w", padx=5)
        self.username_entry = tk.Entry(self.content_frame)
        self.username_entry.pack(fill="x", padx=5, pady=5)

        # Поле для пароля
        tk.Label(self.content_frame, text="Пароль").pack(anchor="w", padx=5)
        self.password_entry = tk.Entry(self.content_frame, show="*")
        self.password_entry.pack(fill="x", padx=5, pady=5)

        # Кнопка для авторизации
        tk.Button(
            self.content_frame, text="Войти", command=self.authenticate_user
        ).pack(pady=10)

        # Кнопка для переключения на форму регистрации
        tk.Button(
            self.content_frame,
            text="У вас еще нет аккаунта? Зарегистрируйтесь",
            command=self.show_registration_form,
        ).pack(pady=10)

    def authenticate_user(self):
        """Метод для авторизации пользователя"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Здесь должна быть логика проверки пользователя
            print(f"Пользователь {username} пытается войти.")
            # Для теста - сообщение
            messagebox.showinfo("Авторизация", f"Пользователь {username} авторизован!")
        else:
            messagebox.showerror("Ошибка", "Введите имя пользователя и пароль!")

    def show_registration_form(self):
        """Показываем форму для регистрации"""
        # Удаляем старое содержимое
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Создаем форму регистрации
        registration_form = RegistrationForm(
            self.content_frame, on_switch_to_login=self.show_login_form
        )
        registration_form.pack(fill="both", expand=True)
