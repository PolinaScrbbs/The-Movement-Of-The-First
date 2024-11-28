from typing import Generator
from sqlalchemy import select

from ..models import User


def get_user_by_username(session: Generator, username: str) -> User:
    result = session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    return user