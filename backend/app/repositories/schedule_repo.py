from sqlalchemy.orm import Session
from app.models.schedule import Schedule

class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Schedule).all()
    
    def get_by_id(self, schedule_id: int):
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
