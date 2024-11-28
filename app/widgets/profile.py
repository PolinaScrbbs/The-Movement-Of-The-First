from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
from PIL import Image, ImageTk

from ..datebase import get_session
from ..models import User
from ..queries import update_user_avatar


class ProfileApp(tk.Toplevel):
    def __init__(self, parent, user: User):
        super().__init__(parent)
        self.title(f"Profile: {user.username}")
        self.geometry("400x400")
        self.parent = parent
        self.user = user

        # Отображаем информацию о пользователе
        self.create_profile_content()

    def create_profile_content(self):
        """Создаем интерфейс профиля"""

        # Загружаем аватарку
        if self.user.avatar_url:
            # Если аватар пользователя указан, загружаем его
            profile_image = Image.open(self.user.avatar_url).resize((100, 100))
        else:
            # Если аватар не указан, используем изображение по умолчанию
            profile_image = Image.open("app/assets/default.jpg").resize((100, 100))

        # Конвертируем изображение для Tkinter
        self.profile_image_tk = ImageTk.PhotoImage(profile_image)

        # Создаём и отображаем Label с изображением
        self.image_label = tk.Label(self, image=self.profile_image_tk, cursor="hand2")
        self.image_label.pack(pady=10)

        # Делаем аватарку кликабельной
        self.image_label.bind("<Button-1>", self.change_avatar)

        username_label = tk.Label(
            self, text=f"@{self.user.username}", font=("Arial", 14)
        )
        username_label.pack(pady=5)

        full_name_label = tk.Label(
            self,
            text=f"{self.user.get_full_name_initials()}",
            font=("Arial", 14),
        )
        full_name_label.pack(pady=5)

        role_label = tk.Label(self, text=f"{self.user.role.value}", font=("Arial", 14))
        role_label.pack(pady=5)

    def change_avatar(self, event):
        """Открывает проводник для выбора нового аватара"""
        file_path = filedialog.askopenfilename(
            title="Выберите аватар",
            filetypes=[("Изображения", "*.jpg *.png")],
        )
        if file_path:
            try:
                # Получаем оригинальное расширение файла
                original_extension = Path(
                    file_path
                ).suffix  # Например, ".jpg" или ".png"

                # Путь для сохранения нового аватара
                new_avatar_path = (
                    f"media/avatars/{self.user.username}{original_extension}"
                )

                # Сохраняем файл в папку с аватарами
                shutil.copy(file_path, new_avatar_path)

                # Проверяем, действительно ли файл сохранён и является изображением
                Image.open(new_avatar_path).verify()  # Проверка целостности изображения

                # Обновляем аватар в базе данных
                user = update_user_avatar(get_session(), self.user, new_avatar_path)
                self.parent.user = user

                # Обновляем изображение на экране
                self.refresh_avatar(new_avatar_path)

                # Уведомляем родительское окно об обновлении аватарки
                self.parent.refresh_navbar_avatar(new_avatar_path)

                messagebox.showinfo("Успех", "Аватар успешно обновлен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить аватар: {e}")

    def refresh_avatar(self, avatar_path):
        """Обновляет аватарку в интерфейсе"""
        profile_image = Image.open(avatar_path).resize((100, 100))
        self.profile_image_tk = ImageTk.PhotoImage(profile_image)
        self.image_label.configure(image=self.profile_image_tk)
