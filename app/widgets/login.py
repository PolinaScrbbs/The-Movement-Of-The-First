import tkinter as tk

from ..datebase import get_session
from ..queries import user_login


class LoginForm(tk.Frame):
    def __init__(self, parent, app, on_switch_to_register):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.on_switch_to_register = on_switch_to_register

        self.pack(pady=10)

        # Заголовок
        tk.Label(self, text="Авторизация", font=("Arial", 18)).pack(pady=10)

        # Поле для имени пользователя
        tk.Label(self, text="Имя пользователя").pack(anchor="w", padx=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(fill="x", padx=5, pady=5)

        # Поле для пароля
        tk.Label(self, text="Пароль").pack(anchor="w", padx=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(fill="x", padx=5, pady=5)

        # Кнопка авторизации
        tk.Button(self, text="Войти", command=self.login).pack(pady=10)

        # Кнопка для перехода к регистрации
        tk.Button(
            self,
            text="У вас еще нет аккаунта? Зарегистрируйтесь",
            command=self.on_switch_to_register,
        ).pack(pady=5)

    def login(self):
        """Обрабатывает авторизацию пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            tk.messagebox.showerror("Ошибка", "Введите имя пользователя и пароль!")
            return

        user, msg = user_login(get_session(), login=username, password=password)

        if user:
            tk.messagebox.showinfo("Авторизация", msg)
            self.on_login_success(app=self.app, user=user)
        else:
            tk.messagebox.showerror("Ошибка авторизациия", msg)

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
        app.footer.pack_forget()
        app.content_frame.pack_forget()

        app.navbar.pack(side=tk.TOP, fill=tk.X)  # Navbar всегда наверху
        app.content_frame.pack(
            side=tk.TOP, fill=tk.BOTH, expand=True
        )  # Контент в центре
        app.footer.pack(side=tk.BOTTOM, fill=tk.X)  # Футер внизу

        # Перезагружаем основной контент
        app.event_app.show_events()
