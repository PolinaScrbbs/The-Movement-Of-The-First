from typing import Generator

from ..models import User
from .schemes import UserCreate


def registration_user(session: Generator, user_create: UserCreate) -> User:

    new_user = User(username=user_create.username, full_name=user_create.full_name)
    new_user.set_password(user_create.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
