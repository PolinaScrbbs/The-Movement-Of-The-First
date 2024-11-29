import bcrypt
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from enum import Enum as BaseEnum


class Base(DeclarativeBase):
    pass


class BaseEnum(BaseEnum):
    @classmethod
    async def values(cls):
        return [member.value for member in cls]


class Role(BaseEnum):
    ADMIN = "Администратор"
    STUDENT = "Студент"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(Enum(Role), default=Role.STUDENT, nullable=False)
    avatar_url = Column(String, default=None)

    created_events = relationship("Event", back_populates="creator")
    marks = relationship("EventMark", back_populates="user")
    stars = relationship("EventStar", back_populates="user")

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    def get_full_name_initials(self) -> str:
        name_parts = self.full_name.split()

        if len(name_parts) >= 2:
            surname = name_parts[0]
            initials = "".join([part[0].upper() + "." for part in name_parts[1:]])
            return f"{surname} {initials}"
        return self.full_name
