from sqlalchemy import Column, Integer, Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.constants import ShiftType, DayOfWeek

class ScheduleEntry(Base):
    __tablename__ = "schedule_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False)
    shift_type = Column(SQLEnum(ShiftType), nullable=False)
    
    # Relationships
    staff = relationship("Staff", back_populates="schedule_entries")
    schedule = relationship("Schedule", back_populates="entries")
