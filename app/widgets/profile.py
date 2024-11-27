import tkinter as tk
from ..models import User


class ProfileApp(tk.Toplevel):
    def __init__(self, parent, user: User):
        super().__init__(parent)
        self.title(f"Profile: {user.username}")
        self.geometry("400x400")
        self.user = user

        # Отображаем информацию о пользователе
        self.create_profile_content()

    def create_profile_content(self):
        """Создаем интерфейс профиля"""
        profile_label = tk.Label(self, text="Profile", font=("Arial", 18))
        profile_label.pack(pady=10)

        username_label = tk.Label(
            self, text=f"Username: {self.user.username}", font=("Arial", 14)
        )
        username_label.pack(pady=5)

        full_name_label = tk.Label(
            self,
            text=f"Full Name: {self.user.get_full_name_initials()}",
            font=("Arial", 14),
        )
        full_name_label.pack(pady=5)

        role_label = tk.Label(
            self, text=f"Role: {self.user.role.value}", font=("Arial", 14)
        )
        role_label.pack(pady=5)

        # if self.user.profile_image:
        #     profile_image = Image.open(self.user.profile_image).resize((100, 100))
        #     self.profile_image_tk = ImageTk.PhotoImage(profile_image)
        #     image_label = tk.Label(self, image=self.profile_image_tk)
        #     image_label.pack(pady=5)
