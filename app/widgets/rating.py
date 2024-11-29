import tkinter as tk
from tkinter import ttk

from ..datebase import get_session
from ..queries import get_users_rating


class RatingApp:
    def __init__(self, app: "BaseApp"):  # type: ignore # noqa: F821
        self.app = app  # Ссылка на основной класс
        self.content_frame = app.content_frame  # Контейнер для отображения контента

        # Параметры пагинации
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = 1

    def create_rating_tree(self, tab):
        """Создает таблицу рейтинга пользователей"""
        self.rating_tree = ttk.Treeview(
            tab, columns=("Username", "Full Name", "Stars"), show="headings"
        )

        # Заголовки столбцов
        self.rating_tree.heading("Username", text="Имя пользователя", anchor="center")
        self.rating_tree.heading("Full Name", text="Полное имя", anchor="center")
        self.rating_tree.heading("Stars", text="Звезды", anchor="center")

        # Настройка стилей
        self.add_style(self.rating_tree)

        # Упаковка таблицы
        self.rating_tree.pack(fill="both", expand=True)

    def add_style(self, treeview):
        """Настройка стилей таблицы"""
        treeview.tag_configure("oddrow", background="#f9f9f9")
        treeview.tag_configure("evenrow", background="#ffffff")

        # Настраиваем столбцы
        for col in treeview["columns"]:
            treeview.column(col, anchor="center", width=120)

    def completion_rating_tree(self):
        """Заполняет таблицу рейтингом для текущей страницы"""
        # Очищаем таблицу
        for item in self.rating_tree.get_children():
            self.rating_tree.delete(item)

        # Получаем пользователей с рейтингом
        users = get_users_rating(get_session())
        self.total_pages = (len(users) + self.items_per_page - 1) // self.items_per_page

        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        users_page = users[start_idx:end_idx]

        # Заполняем таблицу пользователями текущей страницы
        for idx, user in enumerate(users_page):
            row_tag = "oddrow" if idx % 2 == 0 else "evenrow"
            self.rating_tree.insert(
                "",
                "end",
                values=(user.username, user.full_name, user.stars),
                tags=(row_tag,),
            )

    def create_pagination_controls(self):
        """Создает элементы управления пагинацией"""
        control_frame = tk.Frame(self.content_frame)
        control_frame.pack(side="bottom", fill="x", pady=5)

        prev_button = tk.Button(control_frame, text="Назад", command=self.prev_page)
        prev_button.pack(side="left", padx=5)

        next_button = tk.Button(control_frame, text="Вперед", command=self.next_page)
        next_button.pack(side="right", padx=5)

        self.page_label = tk.Label(
            control_frame, text=f"Страница {self.current_page} из {self.total_pages}"
        )
        self.page_label.pack(side="left", padx=5)

    def update_pagination_label(self):
        """Обновляет текст для текущей страницы"""
        self.page_label.config(
            text=f"Страница {self.current_page} из {self.total_pages}"
        )

    def prev_page(self):
        """Переход на предыдущую страницу"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_treeview()

    def next_page(self):
        """Переход на следующую страницу"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh_treeview()

    def refresh_treeview(self):
        """Обновляет данные таблицы и управление"""
        self.completion_rating_tree()
        self.update_pagination_label()

    def show_rating(self):
        """Отображает таблицу рейтинга"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_rating_tree(self.content_frame)
        self.create_pagination_controls()

        # Пересчитаем количество страниц
        users = get_users_rating(get_session())
        self.total_pages = (len(users) + self.items_per_page - 1) // self.items_per_page

        # Заполним таблицу данными
        self.completion_rating_tree()

        # Обновим метку пагинации
        self.update_pagination_label()
