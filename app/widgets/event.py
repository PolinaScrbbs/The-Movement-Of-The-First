import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime


from ..datebase import get_session
from ..queries import get_events, create_event
from ..models import Role, EventType


class EventApp:
    def __init__(self, app: "BaseApp"):  # type: ignore # noqa: F821
        self.app = app  # Ссылка на основной класс для доступа к его методам
        self.content_frame = app.content_frame  # Контейнер для отображения контента

        # Параметры пагинации
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = 1

    def create_events_tree(self, tab):
        """Метод для создания таблицы событий"""
        self.event_tree = ttk.Treeview(
            tab, columns=("Event", "Type", "StartAt"), show="headings"
        )

        # Заголовки столбцов
        self.event_tree.heading("Event", text="Событие", anchor="center")
        self.event_tree.heading("StartAt", text="Начало", anchor="center")
        self.event_tree.heading("Type", text="Тип", anchor="center")

        # Стили для таблицы
        self.add_style(self.event_tree)

        # Настроим упаковку для таблицы
        self.event_tree.pack(fill="both", expand=True)

        # Привязываем событие выбора
        self.event_tree.bind("<<TreeviewSelect>>", self.select_event)

        # Добавляем кнопку добавления события для админов
        if self.app.user.role == Role.ADMIN:
            add_event_button = tk.Button(
                tab, text="Добавить событие", command=self.add_event
            )
            add_event_button.pack(side="bottom", pady=5)

    def add_style(self, treeview):
        """Настройка стилей таблицы"""
        treeview.tag_configure("oddrow", background="#f9f9f9")
        treeview.tag_configure("evenrow", background="#ffffff")

        # Настроим столбцы
        for col in treeview["columns"]:
            treeview.column(col, anchor="center", width=100)

    def completion_events_tree(self):
        """Заполняет таблицу событиями для текущей страницы"""
        # Очищаем таблицу
        for item in self.event_tree.get_children():
            self.event_tree.delete(item)

        # Получаем все события и определяем пагинацию
        events = get_events(get_session())
        self.total_pages = (
            len(events) + self.items_per_page - 1
        ) // self.items_per_page

        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        events_page = events[start_idx:end_idx]

        # Заполняем таблицу событиями текущей страницы
        for idx, event in enumerate(events_page):
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
        """Обновляет данные таблицы и обновляет управление"""
        self.completion_events_tree()
        self.update_pagination_label()

    def select_event(self, event):
        """Обрабатывает выбор строки с событием"""
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = self.event_tree.item(selected_item[0])["values"][0]
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
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_events_tree(self.content_frame)
        self.create_pagination_controls()

        # Пересчитаем количество страниц
        events = get_events(get_session())
        self.total_pages = (
            len(events) + self.items_per_page - 1
        ) // self.items_per_page

        # Заполним таблицу данными
        self.completion_events_tree()

        # Обновим метку пагинации
        self.update_pagination_label()

    def add_event(self):
        """Метод для добавления нового события"""
        # Создаем окно для ввода данных
        add_window = tk.Toplevel(self.app)
        add_window.title("Добавить событие")

        # Название события
        tk.Label(add_window, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(add_window, width=21)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Описание
        tk.Label(add_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(add_window, width=21)
        description_entry.grid(row=1, column=1, padx=10, pady=5)

        # Тип события (раскрывающееся меню)
        tk.Label(add_window, text="Тип:").grid(row=2, column=0, padx=10, pady=5)
        event_type_combobox = ttk.Combobox(add_window, state="readonly", width=18)
        event_type_combobox["values"] = [event_type.name for event_type in EventType]
        event_type_combobox.grid(row=2, column=1, padx=10, pady=5)
        event_type_combobox.set(
            EventType.MEETING.name
        )  # Устанавливаем значение по умолчанию

        # Дата и время начала
        tk.Label(add_window, text="Дата и время начала:").grid(
            row=3, column=0, padx=10, pady=5
        )
        start_at_date = DateEntry(
            add_window, width=18, date_pattern="yyyy-mm-dd", state="normal"
        )
        start_at_date.grid(row=3, column=1, padx=10, pady=5)

        start_at_time_combobox = ttk.Combobox(add_window, state="readonly", width=10)
        start_at_time_combobox["values"] = [
            f"{hour:02d}:{minute:02d}"
            for hour in range(24)
            for minute in range(0, 60, 30)
        ]
        start_at_time_combobox.set("12:00")  # Значение по умолчанию
        start_at_time_combobox.grid(row=3, column=2, padx=10, pady=5)

        # Дата и время окончания
        tk.Label(add_window, text="Дата и время окончания:").grid(
            row=4, column=0, padx=10, pady=5
        )
        end_at_date = DateEntry(
            add_window, width=18, date_pattern="yyyy-mm-dd", state="normal"
        )
        end_at_date.grid(row=4, column=1, padx=10, pady=5)

        end_at_time_combobox = ttk.Combobox(add_window, state="readonly", width=10)
        end_at_time_combobox["values"] = [
            f"{hour:02d}:{minute:02d}"
            for hour in range(24)
            for minute in range(0, 60, 30)
        ]
        end_at_time_combobox.set("12:30")  # Значение по умолчанию
        end_at_time_combobox.grid(row=4, column=2, padx=10, pady=5)

        # Кнопка "Сохранить"
        save_button = tk.Button(
            add_window,
            text="Сохранить",
            command=lambda: self.save_event(
                title_entry.get(),
                event_type_combobox.get(),  # Получаем выбранное значение
                self.app.user.id,
                start_at_date.get_date(),  # Получаем выбранную дату
                start_at_time_combobox.get(),  # Получаем выбранное время начала
                end_at_date.get_date(),  # Получаем выбранную дату
                end_at_time_combobox.get(),  # Получаем выбранное время окончания
                description_entry.get(),
                add_window,
            ),
        )
        save_button.grid(row=5, column=1, padx=10, pady=20)

    def save_event(
        self,
        title: str,
        event_type: str,
        current_user_id: int,
        start_date: datetime.date,
        start_time: str,
        end_date: datetime.date,
        end_time: str,
        description: str,
        add_window: tk.Toplevel,
    ):
        # Формируем объекты datetime для начала и окончания
        start_at = datetime.combine(
            start_date, datetime.strptime(start_time, "%H:%M").time()
        )
        end_at = datetime.combine(end_date, datetime.strptime(end_time, "%H:%M").time())

        # Проверяем корректность данных
        if not title:
            messagebox.showerror("Ошибка", "Название события обязательно.")
            return
        if start_at >= end_at:
            messagebox.showerror(
                "Ошибка",
                "Дата и время окончания должны быть позже даты и времени начала.",
            )
            return

        # Сохраняем событие в базу данных
        try:
            new_event = create_event(
                session=get_session(),
                title=title,
                description=description,
                event_type=event_type,
                creator_id=current_user_id,
                start_at=start_at,
                end_at=end_at,
            )
            messagebox.showinfo(
                "Успех", f"Событие '{new_event.title}' успешно сохранено!"
            )
            add_window.destroy()  # Закрываем окно добавления события
            self.refresh_events()  # Обновляем список событий
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить событие: {e}")

    def refresh_events(self):
        """Обновление списка событий и пагинации"""
        # Загружаем события из базы данных
        session = get_session()
        events = get_events(session)
        session.close()

        # Обновляем общее количество страниц
        self.total_pages = (
            len(events) + self.items_per_page - 1
        ) // self.items_per_page

        # Если текущая страница переполнена, переходим на новую последнюю страницу
        if (self.current_page - 1) * self.items_per_page >= len(events):
            self.current_page = self.total_pages

        # Перезаполняем таблицу
        self.completion_events_tree()

        # Обновляем элементы управления пагинацией
        self.update_pagination_label()
