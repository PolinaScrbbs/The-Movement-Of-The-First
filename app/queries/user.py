from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User


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
    result = session.execute(
        select(User).order_by(User.stars.desc(), User.full_name.asc())
    )

    return result.scalars().all()
