from sqlalchemy.orm import Session
from app.models.staff import Staff

class StaffRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Staff).all()
    
    def get_by_id(self, staff_id: int):
        return self.db.query(Staff).filter(Staff.id == staff_id).first()
    
    def create(self, staff_data: dict):
        staff = Staff(**staff_data)
        self.db.add(staff)
        self.db.commit()
        return staff
