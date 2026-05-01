from sqlalchemy import Column, Integer, String, Date, Time, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.constants import ShiftType, DayOfWeek

class Shift(Base):
    __tablename__ = "shifts"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    date = Column(Date, nullable=False, index=True)
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False)
    shift_type = Column(SQLEnum(ShiftType), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    staff = relationship("Staff", back_populates="shifts")
