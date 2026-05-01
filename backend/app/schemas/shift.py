from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from app.core.constants import ShiftType, DayOfWeek

class ShiftBase(BaseModel):
    staff_id: Optional[int] = None
    date: date
    day_of_week: DayOfWeek
    shift_type: ShiftType
    start_time: time
    end_time: time

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    staff_id: Optional[int] = None
    shift_type: Optional[ShiftType] = None

class Shift(ShiftBase):
    id: int
    
    class Config:
        from_attributes = True
