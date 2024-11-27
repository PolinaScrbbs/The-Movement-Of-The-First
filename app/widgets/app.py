from .base import BaseApp
from .registration import RegistrationForm
from .login import LoginForm


class App(BaseApp):
    def __init__(self):
        super().__init__(user=None)

    def show_login_form(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        login_form = LoginForm(
            self.content_frame,
            app=self,
            on_switch_to_register=self.show_registration_form,
        )
        login_form.pack(fill="both", expand=True)

    def show_registration_form(self):
        """Показываем форму для регистрации"""
        # Удаляем старое содержимое
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Создаем форму регистрации
        registration_form = RegistrationForm(
            self.content_frame, on_switch_to_login=self.show_login_form
        )
        registration_form.pack(fill="both", expand=True)
