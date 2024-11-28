from datetime import datetime
from typing import List, Generator
from sqlalchemy import select

from ..models import Event, EventType


def get_events(session: Generator) -> List[Event]:
    result = session.execute(select(Event).order_by(Event.title))
    events = result.scalars().all()
    return events


def create_event(
    session: Generator,
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
