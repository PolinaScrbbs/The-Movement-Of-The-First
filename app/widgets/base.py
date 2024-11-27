import tkinter as tk
from PIL import Image, ImageTk


class BaseApp(tk.Tk):
    def __init__(self, token=None):
        super().__init__()
        self.title("THE MOVEMENT OF THE FIRST")
        self.geometry("800x600")

        # Создаем навбар
        self.create_navbar(token)

        # Футер
        self.footer = tk.Frame(self, bg="lightgray", height=30)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.footer_label = tk.Label(
            self.footer,
            text="Powered by PolinaScrbbs",
            font=("Arial", 10),
            bg="lightgray",
        )
        self.footer_label.pack(side=tk.RIGHT, padx=10)

        # Основная область контента
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.show_content("Page 1")

    def create_navbar(self, token):
        """Создание навбара в зависимости от наличия токена"""
        self.navbar = tk.Frame(self, bg="lightgray", height=50)
        self.navbar.pack(side=tk.TOP, fill=tk.X)

        self.navbar.columnconfigure(0, weight=1)
        self.navbar.columnconfigure(1, weight=2)
        self.navbar.columnconfigure(2, weight=1)

        # Левый блок (иконка и название)
        self.left_frame = tk.Frame(self.navbar, bg="lightgray")
        self.left_frame.grid(row=0, column=0, sticky="w", padx=10)

        icon_image = Image.open("app/assets/Sunday.png").resize((30, 30))
        self.icon = ImageTk.PhotoImage(icon_image)
        self.icon_label = tk.Label(self.left_frame, image=self.icon, bg="lightgray")
        self.icon_label.pack(side=tk.LEFT)

        self.app_name = tk.Label(
            self.left_frame, text="TMOTF", font=("Arial", 16, "bold"), bg="lightgray"
        )
        self.app_name.pack(side=tk.LEFT, padx=5)

        if token:
            # Центральный блок (кнопки переключения)
            self.center_frame = tk.Frame(self.navbar, bg="lightgray")
            self.center_frame.grid(row=0, column=1)

            self.button1 = tk.Button(
                self.center_frame,
                text="Page 1",
                command=lambda: self.switch_page("Page 1"),
            )
            self.button2 = tk.Button(
                self.center_frame,
                text="Page 2",
                command=lambda: self.switch_page("Page 2"),
            )
            self.button3 = tk.Button(
                self.center_frame,
                text="Page 3",
                command=lambda: self.switch_page("Page 3"),
            )

            self.button1.pack(side=tk.LEFT, padx=5)
            self.button2.pack(side=tk.LEFT, padx=5)
            self.button3.pack(side=tk.LEFT, padx=5)

            # Правый блок (профиль и ник)
            self.right_frame = tk.Frame(self.navbar, bg="lightgray")
            self.right_frame.grid(row=0, column=2, sticky="e", padx=10)

            self.user_name = tk.Label(
                self.right_frame,
                text="PolinaScrbbs",
                font=("Arial", 12),
                bg="lightgray",
            )
            self.user_name.pack(side=tk.LEFT, padx=5)

            self.profile_icon = ImageTk.PhotoImage(icon_image)
            self.profile_label = tk.Label(
                self.right_frame,
                image=self.profile_icon,
                bg="lightgray",
                width=30,
                height=30,
            )
            self.profile_label.pack(side=tk.LEFT)
        else:
            # Правый блок без токена (кнопка "Войти")
            self.right_frame = tk.Frame(self.navbar, bg="lightgray")
            self.right_frame.grid(row=0, column=2, sticky="e", padx=10)

            self.login_button = tk.Button(
                self.right_frame, text="Войти", command=self.login_action
            )
            self.login_button.pack(side=tk.RIGHT, padx=10)

    def switch_page(self, page_name):
        """Переключение контента"""
        self.show_content(page_name)

    def show_content(self, page_name):
        """Обновление основного контента"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.content_frame, text=f"Welcome to {page_name}", font=("Arial", 24)
        )
        label.pack(pady=20)