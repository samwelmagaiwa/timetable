from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.constants import StaffRole

class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(StaffRole), nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    max_hours_per_week = Column(Integer, default=40)
    min_hours_between_shifts = Column(Integer, default=8)
    can_work_night_shift = Column(Boolean, default=True)
    
    # Relationships
    schedule_entries = relationship("ScheduleEntry", back_populates="staff")
    night_tracking = relationship("NightTracking", back_populates="staff")
    shifts = relationship("Shift", back_populates="staff")
