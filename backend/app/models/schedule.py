from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_published = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)  # Lock finalized schedules
    
    # Relationships
    entries = relationship("ScheduleEntry", back_populates="schedule")
    night_tracking = relationship("NightTracking", back_populates="schedule")
