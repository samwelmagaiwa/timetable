from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.core.constants import ShiftType, DayOfWeek

class ScheduleEntryBase(BaseModel):
    schedule_id: int
    staff_id: int
    date: date
    day_of_week: DayOfWeek
    shift_type: ShiftType

class ScheduleEntryCreate(ScheduleEntryBase):
    pass

class ScheduleEntryUpdate(BaseModel):
    shift_type: Optional[ShiftType] = None

class ScheduleEntry(ScheduleEntryBase):
    id: int
    
    class Config:
        from_attributes = True
