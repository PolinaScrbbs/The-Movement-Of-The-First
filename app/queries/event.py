from datetime import datetime
from typing import List
from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from ..models import User, Event, EventType, EventMark


def get_events(session: Session) -> List[Event]:
    result = session.execute(select(Event).order_by(Event.title))
    events = result.scalars().all()
    return events


def create_event(
    session: Session,
    title: str,
    description: str,
    event_type: str,
    creator_id: int,
    start_at: datetime,
    end_at: datetime,
) -> Event:

    new_event = Event(
        title=title,
        description=description,
        type=EventType[event_type],
        creator_id=creator_id,
        start_at=start_at,
        end_at=end_at,
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event


def create_event_mark(session: Session, event_id: int, user_id: int) -> None:
    new_event_mark = EventMark(
        event_id=event_id,
        user_id=user_id,
    )
    session.add(new_event_mark)
    session.commit()
    session.refresh(new_event_mark)


def check_event_mark_exists(session, user_id, event_id):
    stmt = select(
        exists().where(EventMark.user_id == user_id, EventMark.event_id == event_id)
    )
    result = session.execute(stmt).scalar()
    return result


def get_event_attendees(session: Session, event_id):
    try:
        attendees = (
            session.query(User.username, User.full_name, EventMark.created_at)
            .join(EventMark, User.id == EventMark.user_id)
            .filter(EventMark.event_id == event_id)
            .all()
        )
        return attendees
    finally:
        session.close()
