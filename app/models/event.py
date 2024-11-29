from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Enum,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship


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
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        nullable=False,
    )
    end_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        nullable=False,
    )

    creator = relationship("User", back_populates="created_events")
    marks = relationship("EventMark", back_populates="event")


class EventMark(Base):
    __tablename__ = "event_marks"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_user"),)

    event = relationship("Event", back_populates="marks")
    user = relationship("User", back_populates="marks")
