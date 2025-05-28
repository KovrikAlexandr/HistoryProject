from pydantic import BaseModel
from typing import Optional
from datetime import date

# ---------- POST /epics ----------
class EpicCreate(BaseModel):
    epic_id: str
    title: str
    description: str

# ---------- POST /events ----------
class EventCreate(BaseModel):
    epic_id: str
    event_date: Optional[date]
    order_index: int
    text: str

# ---------- POST /dependencies ----------
class DependencyCreate(BaseModel):
    epic_id: str
    depends_on: str
