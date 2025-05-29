from pydantic import BaseModel
from typing import Optional
from datetime import date

class EpicCreate(BaseModel):
    epic_id: str
    title: str
    description: str

class EventCreate(BaseModel):
    epic_id: str
    event_date: date
    text: str

class Dependency(BaseModel):
    epic_id: str
    depends_on_epic_id: str


class EpicPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class EventPatch(BaseModel):
    epic_id: Optional[str] = None
    event_date: Optional[date] = None
    text: Optional[str] = None

