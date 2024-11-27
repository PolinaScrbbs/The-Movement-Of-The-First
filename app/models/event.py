from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP
from sqlalchemy.sql import text


from .user import Base, BaseEnum

class EventType(BaseEnum):
    MEETING = "Встреча"
    REPETITION = "Репетиция"
    PROMOVEMENT = "Продвижение"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(128))
    type = Column(Enum(EventType), default=EventType.MEETING, nullable=False)
    start_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        nullable=False
    )
    end_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        nullable=False
    )