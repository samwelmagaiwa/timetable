from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class NightTracking(Base):
    __tablename__ = "night_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    night_count = Column(Integer, default=0)  # Tracks night shifts per schedule
    last_night_day = Column(Date, nullable=True)  # Last day worked night shift
    rest_until = Column(Date, nullable=True)  # Staff is resting until this date
    
    # Relationships
    staff = relationship("Staff", back_populates="night_tracking")
    schedule = relationship("Schedule", back_populates="night_tracking")
