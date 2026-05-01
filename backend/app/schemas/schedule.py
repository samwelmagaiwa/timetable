from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ScheduleBase(BaseModel):
    name: str
    start_date: date
    end_date: date

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    is_published: Optional[bool] = None
    is_locked: Optional[bool] = None

class Schedule(ScheduleBase):
    id: int
    is_published: bool
    is_locked: bool
    
    class Config:
        from_attributes = True

class ScheduleGenerateRequest(BaseModel):
    start_date: date
    end_date: date
    staff_ids: Optional[List[int]] = None
