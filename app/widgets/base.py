import tkinter as tk
from typing import Optional
from PIL import Image, ImageTk

from app.models.user import Role

from ..models import User
from .profile import ProfileApp
from .event import EventApp
from .rating import RatingApp


class BaseApp(tk.Tk):
    def __init__(self, user: Optional[User] = None):
        super().__init__()
        self.title("THE MOVEMENT OF THE FIRST")
        self.geometry("800x600")
        self.user = user

        # Навбар
        self.create_navbar(self.user)

        # Основная область контента
        self.content_frame = tk.Frame(self, background="#1a76b9")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.show_content("Page 1")

        # Экземпляр EventApp для управления событиями
        self.event_app = EventApp(self)
        self.rating_app = RatingApp(self)

    def create_navbar(self, user: User):
        self.user = user

        """Создание навбара в зависимости от наличия токена"""
        self.navbar = tk.Frame(self, height=50, background="#ffffff")
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        self.navbar.columnconfigure(0, weight=1)
        self.navbar.columnconfigure(1, weight=3)
        self.navbar.columnconfigure(2, weight=1)

        # Левый блок (иконка и название)
        self.left_frame = tk.Frame(self.navbar, background="#ffffff")
        self.left_frame.grid(row=0, column=0, sticky="w")

        # Подготовка иконки
        icon_image = Image.open("app/assets/logo.jpg").resize((225, 75))
        self.icon = ImageTk.PhotoImage(icon_image)

        # Метка с иконкой
        self.icon_label = tk.Label(self.left_frame, image=self.icon, bg="#ffffff")
        self.icon_label.pack(side=tk.LEFT)

        if self.user:
            # Центральный блок (кнопки переключения для администратора)
            self.center_frame = tk.Frame(self.navbar, background="#ffffff")
            self.center_frame.grid(row=0, column=1)

            if self.user.role == Role.ADMIN:
                self.add_event_button = tk.Button(
                    self.center_frame,
                    text="Add Event",  # Кнопка для добавления события
                    command=self.event_app.add_event,  # Метод для добавления события
                    bg="#1a76b9",
                    fg="#ffffff",
                    height=1,  # Высота кнопки
                    width=10,  # Ширина кнопки
                )

                self.add_event_button.pack(side=tk.LEFT, padx=5)

            self.button1 = tk.Button(
                self.center_frame,
                text="Events",  # Кнопка для отображения событий
                command=self.event_app.show_events,  # Используем метод из класса EventApp
                bg="#1a76b9",
                fg="#ffffff",
                height=1,  # Высота кнопки
                width=10,  # Ширина кнопки
            )
            self.button2 = tk.Button(
                self.center_frame,
                text="Rating",
                command=self.rating_app.show_rating,
                bg="#1a76b9",
                fg="#ffffff",
                height=1,  # Высота кнопки
                width=10,  # Ширина кнопки
            )
            self.button1.pack(side=tk.LEFT, padx=5)
            self.button2.pack(side=tk.LEFT, padx=5)

            # Правый блок (профиль и ник)
            self.right_frame = tk.Frame(self.navbar, background="#ffffff")
            self.right_frame.grid(row=0, column=2, sticky="e")

            # Имя пользователя
            self.user_name = tk.Label(
                self.right_frame,
                text=self.user.username,
                font=("Arial", 12),
                bg="#ffffff",
            )
            self.user_name.pack(side=tk.LEFT, padx=5)

            # Проверка на наличие аватарки
            if self.user.avatar_url:
                # Загружаем аватарку пользователя
                icon_image = Image.open(self.user.avatar_url).resize((30, 30))
            else:
                # Используем изображение по умолчанию
                icon_image = Image.open("app/assets/default.jpg").resize((30, 30))

            # Конвертируем изображение для Tkinter
            self.profile_icon = ImageTk.PhotoImage(icon_image)

            # Добавляем метку с аватаркой
            self.profile_label = tk.Label(
                self.right_frame,
                image=self.profile_icon,
                width=30,
                height=30,
                cursor="hand2",  # Сделаем аватар кликабельным
                bg="#ffffff",
            )
            self.profile_label.pack(side=tk.LEFT)

            # При нажатии на аватар переходить в профиль
            self.profile_label.bind("<Button-1>", self.open_profile)

        else:
            # Правый блок без токена (кнопка "Войти")
            self.right_frame = tk.Frame(self.navbar, background="#ffffff")
            self.right_frame.grid(row=0, column=2, sticky="e", padx=10)

    def refresh_navbar_avatar(self, avatar_path):
        """Обновляет аватар в навбаре"""
        # Обновляем аватарку пользователя
        icon_image = Image.open(avatar_path).resize((30, 30))
        self.profile_icon = ImageTk.PhotoImage(icon_image)
        self.profile_label.configure(image=self.profile_icon)

    def open_profile(self, event=None):
        """Открытие окна профиля"""
        if self.user:
            ProfileApp(self, self.user, self)

    def switch_page(self, page_name):
        """Переключение контента"""
        self.show_content(page_name)

    def show_content(self, page_name=None):
        """Обновление основного контента"""
        # Удаляем все виджеты из content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.user:  # Если пользователь не авторизован
            # Родительский контейнер для надписи и кнопки
            container = tk.Frame(self.content_frame, bg="#1a76b9")
            container.place(relx=0.5, rely=0.5, anchor="center")  # Центрируем контейнер

            # Надпись
            label = tk.Label(
                container,
                text="Добро пожаловать в {Название}!\nПожалуйста, авторизуйтесь, чтобы продолжить.",
                font=("Arial", 18),
                justify="center",
                wraplength=600,
                bg="#1a76b9",
                fg="#ffffff",
            )
            label.pack(pady=10)  # Отступ между текстом и кнопкой

            # Кнопка "Войти"
            login_button = tk.Button(
                container,
                text="Войти",
                font=("Arial", 14),
                command=self.login_action,
                width=15,
                height=2,
                background="#ffffff",
            )
            login_button.pack(pady=10)  # Отступ под кнопкой

        else:  # Для авторизованных пользователей
            if page_name is None:  # Если страница не указана, показываем первую
                page_name = "Page 1"

            label = tk.Label(
                self.content_frame,
                text=f"Welcome to {page_name}",
                font=("Arial", 24),
            )
            label.pack(pady=20)

    def login_action(self):
        """Действие при нажатии на кнопку 'Войти'"""
        self.show_login_form()
