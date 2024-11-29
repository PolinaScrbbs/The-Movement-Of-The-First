from typing import List
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from ..models import User, Role, EventStar


def get_user_by_username(session: Session, username: str) -> User:
    result = session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    return user


def update_user_avatar(session: Session, user: User, new_path: str) -> User:
    user = get_user_by_username(session, user.username)

    user.avatar_url = new_path
    session.commit()
    session.refresh(user)

    return user


def get_users_rating(session: Session) -> List[User]:
    # Подсчет звезд на основе таблицы EventStars
    result = session.execute(
        select(User.username, User.full_name, func.count(EventStar.id).label("stars"))
        .where(User.role == Role.STUDENT)
        .join(EventStar, User.id == EventStar.user_id, isouter=True)
        .group_by(User.id)
        .order_by(text("stars DESC"), User.full_name.asc())
    )

    return result.all()
