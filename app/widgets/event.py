import tkinter as tk
from tkinter import ttk
from ..datebase import get_session
from ..queries import get_events


class EventApp:
    def __init__(self, app: "BaseApp"):  # type: ignore # noqa: F821
        self.app = app  # Ссылка на основной класс для доступа к его методам
        self.content_frame = app.content_frame  # Контейнер для отображения контента

    def create_events_tree(self, tab):
        """Метод для создания таблицы событий"""
        self.event_tree = ttk.Treeview(
            tab, columns=("ID", "Event", "Type", "StartAt"), show="headings"
        )

        # Заголовки столбцов
        self.event_tree.heading("ID", text="ID", anchor="center")
        self.event_tree.heading("Event", text="Событие", anchor="center")
        self.event_tree.heading("StartAt", text="Начало", anchor="center")
        self.event_tree.heading("Type", text="Тип", anchor="center")

        # Стили для таблицы
        self.add_style(self.event_tree)

        # Настроим упаковку для таблицы
        self.event_tree.pack(fill="both", expand=True)

        # Привязываем событие выбора
        self.event_tree.bind("<<TreeviewSelect>>", self.select_event)

    def add_style(self, treeview):
        """Настройка стилей таблицы"""
        treeview.tag_configure("oddrow", background="#f9f9f9")
        treeview.tag_configure("evenrow", background="#ffffff")

        # Настроим столбцы
        for col in treeview["columns"]:
            treeview.column(col, anchor="center", width=100)

    def completion_events_tree(self):
        """Заполняет таблицу событиями"""
        # Очищаем таблицу
        for item in self.event_tree.get_children():
            self.event_tree.delete(item)

        # Получаем события
        events = get_events(get_session())

        # Заполняем таблицу событиями
        for idx, event in enumerate(events):
            row_tag = "oddrow" if idx % 2 == 0 else "evenrow"
            self.event_tree.insert(
                "",
                "end",
                values=(
                    event.id,
                    event.title,
                    event.type.value,
                    event.start_at.strftime("%H:%M %d.%m.%Y"),
                ),
                tags=(row_tag,),
            )

    def select_event(self, event):
        """Обрабатывает выбор строки с событием"""
        selected_item = self.event_tree.selection()[0]
        event_id = self.event_tree.item(selected_item)["values"][0]
        print(f"Selected event ID: {event_id}")
        self.show_event_details(event_id)

    def show_event_details(self, event_id):
        """Метод для отображения подробностей события"""
        event = self.get_event_by_id(event_id)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        details_label = tk.Label(
            self.content_frame,
            text=f"Details for {event.title}",
            font=("Arial", 16, "bold"),
        )
        details_label.pack(pady=20)

        description_label = tk.Label(
            self.content_frame,
            text=f"Description: {event.description}",
            font=("Arial", 12),
            anchor="w",
            justify="left",
        )
        description_label.pack(pady=10)

        date_label = tk.Label(
            self.content_frame,
            text=f"Date: {event.start_at}",
            font=("Arial", 12),
            anchor="w",
            justify="left",
        )
        date_label.pack(pady=10)

        back_button = tk.Button(
            self.content_frame, text="Back", command=self.show_events
        )
        back_button.pack(pady=20)

    def get_event_by_id(self, event_id):
        """Получаем событие по ID"""
        # Реализуйте логику поиска события по ID
        return next(
            event for event in get_events(get_session()) if event.id == event_id
        )

    def show_events(self):
        """Метод для отображения списка событий"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_events_tree(self.content_frame)
        self.completion_events_tree()
