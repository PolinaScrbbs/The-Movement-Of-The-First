import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pytz


from ..datebase import get_session
from ..queries import (
    get_events,
    create_event,
    create_event_mark,
    check_event_mark_exists,
    get_event_attendees,
    check_event_star_exists,
    create_event_stars,
)
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

    def add_style(self, treeview):
        style = ttk.Style()
        style.configure(
            "Treeview.Heading", font=("Arial", 11, "bold")
        )  # Шрифт для заголовков
        style.configure("Treeview", font=("Arial", 10))  # Общий шрифт для таблицы
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
        control_frame = tk.Frame(self.content_frame, background="#1a76b9")
        control_frame.pack(side="bottom", fill="x", pady=5)

        prev_button = tk.Button(
            control_frame,
            text="Назад",
            font=("Arial", 10, "bold"),
            background="#ffffff",
            command=self.prev_page,
        )
        prev_button.pack(side="left", padx=5)

        next_button = tk.Button(
            control_frame,
            text="Вперед",
            font=("Arial", 10, "bold"),
            background="#ffffff",
            command=self.next_page,
        )
        next_button.pack(side="right", padx=5)

        # Центральный контейнер для выравнивания текста
        page_label_frame = tk.Frame(control_frame, bg="#1a76b9")
        page_label_frame.pack(side="top", fill="x", padx=5)

        self.page_label = tk.Label(
            page_label_frame,
            text=f"Страница {self.current_page} из {self.total_pages}",
            font=("Arial", 12, "bold"),
            background="#1a76b9",
            fg="#ffffff",
        )
        self.page_label.pack()

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

        # Очистка фрейма
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Настройка общего фона
        self.content_frame.config(bg="#1a76b9")

        # Заголовок события
        details_label = tk.Label(
            self.content_frame,
            text=f"Details for {event.title}",
            font=("Arial", 16, "bold"),
            bg="#1a76b9",
            fg="#ffffff",
        )
        details_label.place(relx=0.5, rely=0.1, anchor="center")

        # Описание события
        description_label = tk.Label(
            self.content_frame,
            text=f"Description: {event.description}",
            font=("Arial", 12, "bold"),  # Жирный текст
            bg="#1a76b9",
            fg="#ffffff",
            anchor="w",
            justify="left",
            wraplength=400,  # Перенос текста, если он слишком длинный
        )
        description_label.place(relx=0.5, rely=0.2, anchor="center")

        # Форматированная дата начала
        formatted_start_date = event.start_at.strftime("%H:%M %d.%m.%Y")
        start_date_label = tk.Label(
            self.content_frame,
            text=f"Start At: {formatted_start_date}",
            font=("Arial", 12, "bold"),  # Жирный текст
            bg="#1a76b9",
            fg="#ffffff",
            anchor="w",
            justify="left",
        )
        start_date_label.place(relx=0.5, rely=0.3, anchor="center")

        # Форматированная дата окончания
        formatted_end_date = event.end_at.strftime("%H:%M %d.%m.%Y")
        end_date_label = tk.Label(
            self.content_frame,
            text=f"End At: {formatted_end_date}",
            font=("Arial", 12, "bold"),  # Жирный текст
            bg="#1a76b9",
            fg="#ffffff",
            anchor="w",
            justify="left",
        )
        end_date_label.place(relx=0.5, rely=0.4, anchor="center")

        # Проверка времени события и добавление кнопки "Отметиться"
        now = datetime.now(pytz.timezone("Europe/Moscow"))
        start_at = event.start_at
        end_at = event.end_at

        if (
            self.app.user
            and self.app.user.role == Role.STUDENT
            and not check_event_mark_exists(get_session(), self.app.user.id, event_id)
            and start_at <= now <= end_at
        ):
            check_in_button = tk.Button(
                self.content_frame,
                text="Отметиться",
                command=lambda: self.mark_attendance(event_id),
                bg="#ffffff",
                fg="#1a76b9",
            )
            check_in_button.place(relx=0.5, rely=0.5, anchor="center")

        # Если пользователь - администратор, отображаем список отметившихся
        if self.app.user and self.app.user.role == Role.ADMIN:
            attendees_label = tk.Label(
                self.content_frame,
                text="Отметившиеся пользователи:",
                font=("Arial", 14, "bold"),
                bg="#1a76b9",
                fg="#ffffff",
            )
            attendees_label.place(relx=0.5, rely=0.5, anchor="center")

            # Получение списка отметившихся
            attendees = get_event_attendees(get_session(), event_id)

            if attendees:
                # Создание Treeview только если есть отметившиеся
                tree_frame = tk.Frame(self.content_frame, bg="#1a76b9")
                tree_frame.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8, relheight=0.3)

                style = ttk.Style()
                style.configure("Treeview", rowheight=25)
                style.configure(
                    "Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    anchor="center",  # Выровнять заголовки по центру
                )
                style.configure("Treeview", font=("Arial", 10), anchor="center")  # Выровнять строки

                tree = ttk.Treeview(
                    tree_frame,
                    columns=("username", "fullname", "timestamp", "action"),
                    show="headings",
                )
                tree.heading("username", text="Username", anchor="center")
                tree.heading("fullname", text="Full Name", anchor="center")
                tree.heading("timestamp", text="Marked At", anchor="center")
                tree.heading("action", text="Action", anchor="center")
                tree.column("username", width=150, anchor="center")
                tree.column("fullname", width=200, anchor="center")
                tree.column("timestamp", width=150, anchor="center")
                tree.column("action", width=100, anchor="center")
                tree.pack(side="left", fill="both", expand=True)

                # Добавление прокрутки
                scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
                scrollbar.pack(side="right", fill="y")
                tree.configure(yscrollcommand=scrollbar.set)

                # Добавление данных
                for attendee in attendees:
                    has_star = check_event_star_exists(
                        get_session(), attendee.id, event_id
                    )

                    action_text = "Звезда выдана" if has_star else "Добавить звезду"
                    button_state = tk.DISABLED if has_star else tk.NORMAL

                    row_id = tree.insert(
                        "",
                        "end",
                        values=(
                            attendee.username,
                            attendee.full_name,
                            attendee.created_at.strftime("%H:%M:%S %Y-%m-%d"),
                            action_text,
                        ),
                    )

            else:
                # Если никто не отметился
                no_attendees_label = tk.Label(
                    self.content_frame,
                    text="Список отметок пуст",
                    font=("Arial", 12),
                    bg="#1a76b9",
                    fg="#ffffff",
                    anchor="w",
                )
                no_attendees_label.place(relx=0.5, rely=0.6, anchor="center")

        # Кнопка "Назад"
        back_button = tk.Button(
            self.content_frame,
            text="Back",
            font=("Arial", 10, "bold"),
            command=self.show_events,
            bg="#ffffff",
            width=10,
            height=1
        )
        back_button.place(relx=0.5, rely=0.9, anchor="center")



    def add_star(self, event_id, user_id, tree, row_id):
        """Добавить звезду пользователю"""
        create_event_stars(get_session(), event_id, user_id)
        tree.set(row_id, column="action", value="Звезда выдана")

    def mark_attendance(self, event_id):
        """Метод для отметки пользователя на событии"""
        try:
            # Здесь должна быть логика для отметки пользователя
            # Например, создание записи в базе данных
            create_event_mark(get_session(), event_id, self.app.user.id)
            tk.messagebox.showinfo("Success", "Вы успешно отметились!")
            self.show_event_details(event_id)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Ошибка: {e}")

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
        add_window.config(bg="#1a76b9")

        # Установка сетки для главного контейнера
        add_window.grid_rowconfigure(0, weight=1)
        add_window.grid_columnconfigure(0, weight=1)

        # Основной контейнер для выравнивания содержимого
        container = tk.Frame(add_window, bg="#1a76b9")
        container.grid(row=0, column=0, padx=20, pady=20)
        container.grid_columnconfigure(1, weight=1)

        # Заголовок
        tk.Label(
            container,
            text="Добавить событие",
            font=("Arial", 18, "bold"),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # Поле для названия события
        tk.Label(
            container,
            text="Название:",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=1, column=0, sticky="w", pady=5)
        title_entry = tk.Entry(container, width=30, font=("Arial", 12))
        title_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=10)

        # Поле для описания события
        tk.Label(
            container,
            text="Описание:",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=2, column=0, sticky="w", pady=5)
        description_entry = tk.Entry(container, width=30, font=("Arial", 12))
        description_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=10)

        # Тип события (раскрывающееся меню)
        tk.Label(
            container,
            text="Тип:",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=3, column=0, sticky="w", pady=5)
        event_type_combobox = ttk.Combobox(container, state="readonly", font=("Arial", 12), width=27)
        event_type_combobox["values"] = [event_type.name for event_type in EventType]
        event_type_combobox.grid(row=3, column=1, columnspan=2, pady=5, padx=10)
        event_type_combobox.set(EventType.MEETING.name)  # Значение по умолчанию

        # Дата и время начала
        tk.Label(
            container,
            text="Дата и время начала:",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=4, column=0, sticky="w", pady=5)
        start_at_date = DateEntry(
            container, width=15, date_pattern="yyyy-mm-dd", state="normal", font=("Arial", 12)
        )
        start_at_date.grid(row=4, column=1, pady=5, padx=10, sticky="w")
        start_at_time_combobox = ttk.Combobox(container, state="readonly", font=("Arial", 12), width=10)
        start_at_time_combobox["values"] = [
            f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 30)
        ]
        start_at_time_combobox.set("12:00")
        start_at_time_combobox.grid(row=4, column=2, pady=5, padx=10, sticky="w")

        # Дата и время окончания
        tk.Label(
            container,
            text="Дата и время окончания:",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        ).grid(row=5, column=0, sticky="w", pady=5)
        end_at_date = DateEntry(
            container, width=15, date_pattern="yyyy-mm-dd", state="normal", font=("Arial", 12)
        )
        end_at_date.grid(row=5, column=1, pady=5, padx=10, sticky="w")
        end_at_time_combobox = ttk.Combobox(container, state="readonly", font=("Arial", 12), width=10)
        end_at_time_combobox["values"] = [
            f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 30)
        ]
        end_at_time_combobox.set("12:30")
        end_at_time_combobox.grid(row=5, column=2, pady=5, padx=10, sticky="w")

        # Кнопка "Сохранить"
        save_button = tk.Button(
            container,
            text="Сохранить",
            bg="#ffffff",
            font=("Arial", 14),
            command=lambda: self.save_event(
                title_entry.get(),
                event_type_combobox.get(),
                self.app.user.id,
                start_at_date.get_date(),
                start_at_time_combobox.get(),
                end_at_date.get_date(),
                end_at_time_combobox.get(),
                description_entry.get(),
                add_window,
            ),
            width=20,
            height=1,
        )
        save_button.grid(row=6, column=0, columnspan=3, pady=20)

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
