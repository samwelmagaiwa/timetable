from pydantic import BaseModel
from typing import Optional
from app.core.constants import StaffRole

class StaffBase(BaseModel):
    name: str
    role: StaffRole
    email: str
    phone: Optional[str] = None
    max_hours_per_week: int = 40
    min_hours_between_shifts: int = 8

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[StaffRole] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    max_hours_per_week: Optional[int] = None
    min_hours_between_shifts: Optional[int] = None

class Staff(StaffBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True
