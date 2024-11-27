from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Event

def get_events(session: Session) -> List[Event]:
    result = session.execute(select(Event).order_by(Event.title))
    events = result.scalars().all()
    return events