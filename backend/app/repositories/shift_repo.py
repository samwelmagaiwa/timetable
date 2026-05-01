from sqlalchemy.orm import Session
from app.models.shift import Shift
from datetime import date

class ShiftRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_date_range(self, start_date: date, end_date: date):
        return self.db.query(Shift).filter(Shift.date >= start_date, Shift.date <= end_date).all()
    
    def get_by_staff_id(self, staff_id: int):
        return self.db.query(Shift).filter(Shift.staff_id == staff_id).all()
