from datetime import datetime
from .user import BaseModel, ID
from ...models import EventType


class TitleAndDesc(BaseModel):
    title: str
    description: str


class EventInDB(TitleAndDesc, ID):
    type: EventType
    start_at: datetime
    start_at: datetime
