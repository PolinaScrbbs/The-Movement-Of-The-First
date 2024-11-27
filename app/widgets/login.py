import tkinter as tk

class LoginForm(tk.Frame):
    def __init__(self, parent, on_login, on_switch_to_register):
        super().__init__(parent)
        self.on_login = on_login
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
        tk.Button(self, text="У вас еще нет аккаунта? Зарегистрируйтесь",
                  command=self.on_switch_to_register).pack(pady=5)

    def login(self):
        """Обрабатывает авторизацию пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            tk.messagebox.showerror("Ошибка", "Введите имя пользователя и пароль!")
            return

        self.on_login(username, password)