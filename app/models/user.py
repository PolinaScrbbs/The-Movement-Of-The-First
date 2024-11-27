from typing import Generator
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
import pytz
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import DeclarativeBase
from enum import Enum as BaseEnum

from config import SECRET_KEY


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

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )
