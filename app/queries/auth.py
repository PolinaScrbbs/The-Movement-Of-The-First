from typing import Generator, Optional, Tuple
from tkinter import messagebox

from ..models import User
from .schemes import UserCreate
from .user import get_user_by_username


def registration_user(session: Generator, user_create: UserCreate) -> User:
    new_user = User(username=user_create.username, full_name=user_create.full_name)
    new_user.set_password(user_create.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def user_login(session: Generator, login: str, password: str) -> Tuple[Optional[User], str]:
    user = get_user_by_username(session, login)
    if user is None:
        return None, "Пользователь не найден"

    correct_password = user.check_password(password)
    if not correct_password:
        return None, "Неверный пароль"

    return user, f"С возвращением, {user.username}"
