from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
from PIL import Image, ImageTk

from ..datebase import get_session
from ..models import User
from ..queries import update_user_avatar


class ProfileApp(tk.Toplevel):
    def __init__(self, parent, user: User, app):
        super().__init__(parent)
        self.title(f"Профиль: {user.username}")
        self.geometry("400x400")
        self.parent = parent
        self.user = user
        self.app = app  # Сохраняем ссылку на приложение

        # Установка фона
        self.configure(bg="#1a76b9")

        # Отображаем информацию о пользователе
        self.create_profile_content()

    def create_profile_content(self):
        """Создаем интерфейс профиля"""

        # Основной контейнер для выравнивания содержимого
        container = tk.Frame(self, bg="#1a76b9")
        container.pack(expand=True, fill="both", pady=20)

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
        self.image_label = tk.Label(
            container,
            image=self.profile_image_tk,
            bg="#1a76b9",
            cursor="hand2",
        )
        self.image_label.pack(pady=10)

        # Делаем аватарку кликабельной
        self.image_label.bind("<Button-1>", self.change_avatar)

        # Имя пользователя
        username_label = tk.Label(
            container,
            text=f"@{self.user.username}",
            font=("Arial", 14, "bold"),
            bg="#1a76b9",
            fg="#ffffff",
        )
        username_label.pack(pady=5)

        # Полное имя пользователя
        full_name_label = tk.Label(
            container,
            text=f"{self.user.get_full_name_initials()}",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        )
        full_name_label.pack(pady=5)

        # Роль пользователя
        role_label = tk.Label(
            container,
            text=f"{self.user.role.value}",
            font=("Arial", 12),
            bg="#1a76b9",
            fg="#ffffff",
        )
        role_label.pack(pady=5)

        # Кнопка выхода (например)
        tk.Button(
            container,
            text="Выйти",
            bg="#ffffff",
            font=("Arial", 14),
            command=self.logout,
            height=1,
            width=20,
        ).pack(pady=20)

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

    def logout(self):
        """Функция выхода"""
        if messagebox.askyesno("Подтверждение", "Вы действительно хотите выйти?"):
            # Закрываем приложение
            self.app.destroy()

            # Перезапуск приложения
            self.app = self.app.__class__()  # Создаем новый экземпляр класса App
            self.app.mainloop()


