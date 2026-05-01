from pydantic import BaseModel
from typing import Optional
from datetime import date

class NightTrackingBase(BaseModel):
    staff_id: int
    schedule_id: int
    night_count: int = 0
    last_night_day: Optional[date] = None
    rest_until: Optional[date] = None

class NightTracking(NightTrackingBase):
    id: int
    
    class Config:
        from_attributes = True
